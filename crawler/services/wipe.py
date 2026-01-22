from crawler.models import URL

'''
For convenience, wipe the db
'''

def wipe():
    URL.objects.all().delete()