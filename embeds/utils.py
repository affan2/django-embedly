import re
import embeds
from embedly import Embedly

def detect_embedded_content(text):
    results = []

    client = Embedly(key=embeds.EMBEDLY_KEY, user_agent=embeds.USER_AGENT)
    for url in re.findall(embeds.EMBED_REGEX, text):
        results.append(client.oembed(url))

    return results
