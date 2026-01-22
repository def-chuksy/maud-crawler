import requests

'''
fetch html data
possible extension:
'''
def fetch(url: str) -> dict:
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        return {
            "html": res.text
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"{e}") from e 