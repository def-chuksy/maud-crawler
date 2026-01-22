import pytest
from crawler.services.save import save
from crawler.models import URL

MOCK_URLS = [
    "http://maud.crawler/contact.html",
    "https://www.twitter.com",
    "http://maud.crawler/services.html",
    "http://maud.crawler/blog.html",
    "mailto:test@example.com",
    "tel:+19991234567",
]

@pytest.mark.django_db
def test_save():
    urls = save("http://maud.crawler/", MOCK_URLS)

    assert len(urls) == 3
    assert URL.objects.filter(url="http://maud.crawler/contact.html").count() == 1
    assert URL.objects.filter(url="https://www.twitter.com").count() == 0