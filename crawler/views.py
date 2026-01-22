from django.shortcuts import render, redirect
from .services.orchestrator import run
from .services.wipe import wipe
import threading

# Create your views here.
def index(request):
    message = None

    if request.method == 'POST':
        action = request.POST.get("action")

        if action == "crawl":
            seed_url = request.POST.get('seed_url')

            if seed_url:
                #start crawl in thread
                thread = threading.Thread(target=run, args=(seed_url,))
                thread.start()

                return redirect('crawl')
            
        elif action == "wipe":
            wipe()
            return redirect('index')

    return render(request, 'index.html')

def crawl(request):
    return render(request, "crawl.html")