from crawler.models import URL
from asgiref.sync import sync_to_async

'''
serves as a queue, URL frontier
'''

@sync_to_async
def seed(url: str):
    '''
    add seed url to db
    '''
    URL.objects.get_or_create(url=url)

@sync_to_async
def mark_visited(url: str):
    '''
    mark url as visited
    '''
    URL.objects.filter(url=url).update(visited=True, processing=False)

@sync_to_async
def dequeue():
    next_url = URL.objects.filter(visited=False).order_by("created_at").first()
    if next_url:
        next_url.processing = True
        next_url.save(update_fields=["processing"])
    return next_url

@sync_to_async
def queue_has_items():
    return URL.objects.filter(visited=False).exists()

@sync_to_async
def queue_size():
    return URL.objects.filter(visited=False, processing=False).count()

