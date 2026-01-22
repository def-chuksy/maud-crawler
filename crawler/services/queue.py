from crawler.models import URL

'''
serves as a queue, URL frontier
'''

def seed(url: str):
    '''
    add seed url to db
    '''
    URL.objects.create(url=url)

def mark_visited(url: str):
    '''
    mark url as visited
    '''
    URL.objects.filter(url=url).update(visited=True)

def dequeue():
    next_url = URL.objects.filter(visited=False).order_by("created_at").first()
    return next_url

