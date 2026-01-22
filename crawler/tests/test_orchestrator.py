from unittest.mock import patch
from crawler.services.orchestrator import crawl

def test_crawl_execution():
    seed_url = "http://maud.crawler/"

    fake_html = {"html": "<html></html>"}
    parsed_urls = [
        "http://maud.crawler/about",
        "http://maud.crawler/contact",
        "mailto:test@example.com",
    ]
    saved_urls = {
        "http://maud.crawler/about",
        "http://maud.crawler/contact",
    }

    with patch("crawler.services.orchestrator.fetch", return_value=fake_html) as mock_fetch, \
        patch("crawler.services.orchestrator.parse", return_value=parsed_urls) as mock_parse, \
        patch("crawler.services.orchestrator.save", return_value=saved_urls) as mock_save:

        result = crawl(seed_url)

    # assert functions are called
    mock_fetch.assert_called_once_with(seed_url)
    mock_parse.assert_called_once_with(seed_url, fake_html["html"])
    mock_save.assert_called_once_with(seed_url, parsed_urls)
