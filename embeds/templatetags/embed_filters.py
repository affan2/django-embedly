import re
from datetime import datetime
from hashlib import md5

from django import template
from django.core.cache import cache
from django.conf import settings

from embedly import Embedly
from embeds.models import SavedEmbed
from django.utils.safestring import mark_safe
import string


register = template.Library()

EMBED_REGEX = re.compile(r'https?://[\w\d:#@%/;$()~_?\+\-=\\\.&]+', re.I)
USER_AGENT = 'Mozilla/5.0 (compatible; django-embedly/0.2; ' \
        '+http://github.com/jskopek/)'

@register.filter
def embedly(html, arg=None):
    return mark_safe(EMBED_REGEX.sub(lambda x: embed_replace(x, maxwidth=arg), html))


def embed_replace(match, maxwidth=None):
    url = match.group(0)

    key = make_cache_key(url, maxwidth)
    cached_html = cache.get(key)

    if cached_html:
        return cached_html

    # call embedly API
    client = Embedly(key=settings.EMBEDLY_KEY, user_agent=USER_AGENT)
    if maxwidth:
        oembed = client.oembed(url, maxwidth=maxwidth)
    else:
        oembed = client.oembed(url)

    # check database
#    if oembed.error:
#        try:
#            html = SavedEmbed.objects.get(url=url, maxwidth=maxwidth).html
#            cache.set(key, html)
#            return html
#        except SavedEmbed.DoesNotExist:
#            return 'Error embedding %s' % url

    # save result to database
#    row, created = SavedEmbed.objects.get_or_create(url=url, maxwidth=maxwidth,
#                defaults={'type': oembed.type})

    if oembed['type'] == 'photo':
        template = """
        <div class="embeds"><img src="${url}"" /></div>
        """
    elif oembed['type'] == 'link':
        template = """
        <div class="embeds">
            <a href="${url}">
            <img class="embeds-thumbnail" src="${thumbnail_url}" />
            <div class="embeds-text">
                <span class="embeds-title">${title}</span>
                <p class="embeds-description">${description}</p>
                <span class="embeds-source">Read the article on ${provider_url}</span>
            </div>
            </a>
        </div>"""
    elif oembed.get('html'):
        template = """<div class="embeds">${html}</div>"""
    else:
        template = """<a href="${url}">${url}</a>"""
        html = url

    html = string.Template(template).substitute(oembed)

    #if html:
        #row.html = html
        #row.last_updated = datetime.now()
        #row.save()

    # set cache
    #cache.set(key, html, 86400)
    return html


def make_cache_key(url, maxwidth=None):
    md5_hash = md5(url).hexdigest()
    return "embeds.%s.%s" % (maxwidth if maxwidth else 'default', md5_hash)
