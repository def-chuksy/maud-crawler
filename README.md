# crawler
A simple web crawler that given a seed url, crawls that webpage and all the urls founded within that webpage

## Installation

```bash
git clone <repo_url>
```

Setup virtualenv and activate

```bash
python3 -m venv myenv
source myenv/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

Startup the django backend

```bash
python manage.py migrate
python manage.py runserver
```

Visit localhost on port 8000

(Use wipe DB button to clear database if re-testing the same URL)
