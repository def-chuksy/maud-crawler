import logging
import asyncio
import aiohttp
from .fetch import fetch
from .parser import parse
from .save import save
from .queue import dequeue, seed, queue_has_items, queue_size


import sys
logging.basicConfig(
    level=logging.INFO,  # INFO and above
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def crawl(url: str, fetch_sem: asyncio.Semaphore, save_sem: asyncio.Semaphore, session: aiohttp.ClientSession):
    logger.info(f"Starting crawl for {url}")

    try:
        async with fetch_sem:
            logger.info(f"[FETCH] Acquired fetch semaphore for {url}")
            content = await fetch(url, session)
            logger.info(f"[FETCH] Completed fetch for {url}")
    except Exception as e:
        logger.error(f"[FETCH] Failed for {url}: {e}")
        return

    logger.info(f"[PARSE] Parsing URL: {url}")
    urls = parse(url, content["html"])
    logger.info(f"[PARSE] Found {len(urls)} URLs at {url}")

    async with save_sem:
        logger.info(f"[SAVE] Acquired save semaphore for {url}")
        saved_urls = await save(url, urls)
        #await mark_visited(url)
        logger.info(f"[SAVE] Saved URLs from {url}: {saved_urls}")
        logger.info(f"[VISIT] Marked {url} as visited")

async def worker(fetch_sem: asyncio.Semaphore, save_sem: asyncio.Semaphore, stop_event: asyncio.Event, worker_id: int, session: aiohttp.ClientSession):
    logger.info(f"[WORKER-{worker_id}] Started")
    while not stop_event.is_set():
        next_url = await dequeue()
        if not next_url:
            await asyncio.sleep(0.1)
            continue

        logger.info(f"[WORKER-{worker_id}] Picked URL: {next_url.url}")
        await crawl(next_url.url, fetch_sem, save_sem, session)
    logger.info(f"[WORKER-{worker_id}] Stopped")


async def run(seed_url: str):
    logger.info(f"[RUN] Seeding initial URL: {seed_url}")
    await seed(seed_url)

    fetch_sem = asyncio.Semaphore(50)  # concurrent fetch limit
    save_sem = asyncio.Semaphore(2)    # concurrent save limit
    stop_event = asyncio.Event()

    async with aiohttp.ClientSession() as session:

        # workers
        num_workers = 70
        workers = [
            asyncio.create_task(worker(fetch_sem, save_sem, stop_event, i, session))
            for i in range(num_workers)
        ]
        logger.info(f"[RUN] Started {num_workers} workers")

        # Monitor loop
        empty_cycles = 0
        while True:
            size = await queue_size()
            logger.info(f"[MONITOR] URLs left in queue: {size}")

            if await queue_has_items():
                empty_cycles = 0
            else:
                empty_cycles += 1
                logger.info(f"[MONITOR] Queue empty, empty_cycles={empty_cycles}")

            if empty_cycles > 50:  # ~5 seconds idle
                logger.info("[MONITOR] Queue idle, stopping workers")
                stop_event.set()
                break

            await asyncio.sleep(0.1)

        # Wait for all workers to finish
        await asyncio.gather(*workers)
        logger.info("[RUN] ALL DONE!!")
