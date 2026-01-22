import logging
from .fetch import fetch
from .parser import parse
from .save import save
from .queue import dequeue, seed, mark_visited

'''
Main execution process
'run' initiates the execution loop
'crawl' handles actual crawl for each url
'''

logger = logging.getLogger(__name__)

def crawl(url: str):
    try:
        content = fetch(url)
    except Exception as e:
        logger.error(f"Fetch failed: {e}")
        return

    urls = parse(url, content["html"])
    saved_urls = save(url, urls)
    logger.info(f'\nVisited "{url}", found the following urls {saved_urls}')

def run(seed_url: str):
    seed(seed_url)

    while True:
        next_url = dequeue()
        if not next_url:
            break
        crawl(next_url.url)
        mark_visited(next_url.url)
    logger.info("WE'RE DONE!!")