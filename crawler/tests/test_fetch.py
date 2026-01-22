import pytest
from crawler.services.fetch import fetch
from unittest.mock import Mock, patch
from requests.exceptions import RequestException

def test_fetch_success():
    mock_response = Mock()
    mock_response.text = "<html>success</html>"
    mock_response.raise_for_status = Mock()
    
    with patch("requests.get", return_value=mock_response):
        response = fetch("http://maud.crawler/test/fetch")

    assert response['html'] == "<html>success</html>"

def test_fetch_failure():
    with patch("requests.get", side_effect=RequestException):
        with pytest.raises(Exception):
            fetch("http://maud.crawler/test/fetch")