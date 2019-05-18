import datetime
from hashlib import md5

from django import template
from django.core.cache import cache
from django.utils import timezone

import embeds
from embedly import Embedly
from embeds.models import SavedEmbed
from django.utils.safestring import mark_safe
import string

now = timezone.now

register = template.Library()


@register.filter
def embedly(html, arg=None):
    return mark_safe(embeds.EMBED_REGEX.sub(lambda x: embed_replace(x, maxwidth=arg), html))


def embed_replace(match, maxwidth=None):
    url = match.group(0)

    key = make_cache_key(url, maxwidth)
    cached_html = cache.get(key)

    if cached_html:
        return cached_html

    # check database
    try:
        html = SavedEmbed.objects.get(
            url=url,
            maxwidth=maxwidth,
            last_updated__gt=now() - datetime.timedelta(seconds=embeds.CACHE_TIMEOUT)
        ).html
        cache.set(key, html, embeds.CACHE_TIMEOUT)
        return html
    except SavedEmbed.DoesNotExist:
        pass

    # call embedly API
    client = Embedly(key=embeds.EMBEDLY_KEY, user_agent=embeds.USER_AGENT)
    if maxwidth:
        oembed = client.oembed(url, maxwidth=maxwidth)
    else:
        oembed = client.oembed(url)

    if oembed.get('error'):
        return 'Error embedding %s' % url

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

    # Set up defaults and populate with data
    data = {
        'title': '',
        'url': '',
        'thumbnail_url': embeds.DEFAULT_THUMBNAIL,
        'description': '',
        'provider_url': '?'
    }
    data.update(oembed)

    html = string.Template(template).substitute(data)

    # save result to database
    row, created = SavedEmbed.objects.get_or_create(url=url, maxwidth=maxwidth, defaults={
        'type': oembed['type'],
        'html': html
    })

    if not created:
        row.save()

    # set cache
    cache.set(key, html, embeds.CACHE_TIMEOUT)

    return html


def make_cache_key(url, maxwidth=None):
    md5_hash = md5(url.encode('utf-8')).hexdigest()
    return "embeds.%s.%s" % (maxwidth if maxwidth else 'default', md5_hash)
