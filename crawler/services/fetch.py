import aiohttp
import asyncio
import logging

logger = logging.getLogger(__name__)

async def fetch(url: str, session: aiohttp.ClientSession) -> dict:
    """
    Async fetch using a shared aiohttp session.
    Returns a dict with 'html' key.
    """
    try:
        logger.info(f"Starting async HTTP request for {url}")
        async with session.get(url, timeout=10) as resp:
            resp.raise_for_status()
            html = await resp.text()
            logger.info(f"Completed async fetch for {url}")
            return {"html": html}

    except aiohttp.ClientError as e:
        logger.error(f"HTTP request failed for {url}: {e}")
        raise
    except asyncio.TimeoutError:
        logger.error(f"HTTP request timed out for {url}")
        raise
