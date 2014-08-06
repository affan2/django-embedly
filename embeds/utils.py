import re
from embeds import EMBEDLY_KEY, EMBED_REGEX, USER_AGENT

from embedly import Embedly


def detect_embedded_content(text):
    results = []

    client = Embedly(key=EMBEDLY_KEY, user_agent=USER_AGENT)
    for url in re.findall(EMBED_REGEX, text):
        results.append(client.oembed(url))

    return results
