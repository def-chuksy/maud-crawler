from crawler.models import URL
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

'''
save data(list of urls)
'''
def save(url: str, urls: list) -> list:
    
    #filter out urls not in subdomain and non-http(s)
    base_netloc = urlparse(url).netloc
    urls = {url for url in urls 
            if urlparse(url).netloc == base_netloc and
            urlparse(url).scheme in ("http", "https")}

    #add URLs to DB
    URL.objects.bulk_create(
        [URL(url=url) for url in urls],
        ignore_conflicts=True
    )

    # return urls found on this page (for printing/logging)
    return urls