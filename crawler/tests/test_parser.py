from crawler.services.parser import parse

MOCK_HTML = """
<html>
  <head>
    <title>Test Page</title>
  </head>
  <body>
    <a href="/about">About</a>
    <a href="contact.html">Contact</a>
    <a href="https://www.twitter.com">Twitter</a>
    <a href="services.html">Our Services</a>
    <a href="blog.html">Read Our Blog</a>
    <a href="mailto:test@example.com">Email</a>
    <a href="tel:+19991234567">Phone</a>
    <a href="/about">Duplicate About</a>

    <div>
      <p>No link here</p>
    </div>
  </body>
</html>
"""

def test_parse():
    urls = parse("crawlme.monzo.com", MOCK_HTML)
    
    assert type(urls) == list
    assert "contact.html" in urls

