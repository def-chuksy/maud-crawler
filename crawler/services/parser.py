from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urldefrag

'''
parser html data, getting all urls
Possible extension:
filter for other types of links: media (images, video)
'''
logger = logging.getLogger(__name__)

def parse(base_url: str, html: str) -> list:
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    hrefs = [a_tag.get("href") for a_tag in soup.find_all("a", href=True)]
    for href in hrefs:
        url = urljoin(base_url, href)
        url, _ = urldefrag(url)
        url = url.rstrip("/")
        urls.append(url)
    return urls