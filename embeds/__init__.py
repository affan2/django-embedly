from django.conf import settings
import re

EMBED_REGEX = re.compile(r'https?://[\w\d:#@%/;$()~_?\+\-=\\\.&]+', re.I)

try:
    USER_AGENT = settings.EMBEDLY_USER_AGENT
except AttributeError:
    USER_AGENT = 'Mozilla/5.0 (compatible; django-embedly/0.2; +http://github.com/jskopek/)'

try:
    DEFAULT_THUMBNAIL = settings.EMBEDLY_DEFAULT_THUMBNAIL
except AttributeError:
    DEFAULT_THUMBNAIL = ''

try:
    EMBEDLY_KEY = settings.EMBEDLY_KEY
except AttributeError:
    EMBEDLY_KEY = ''

    import logging
    logger = logging.getLogger(__name__)
    logger.error('`EMBEDLY_KEY` property not found in Django Settings')


