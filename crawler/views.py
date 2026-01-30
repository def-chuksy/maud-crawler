from django.shortcuts import render, redirect
from .services.orchestrator import run
from .services.wipe import wipe

async def index(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "crawl":
            seed_url = request.POST.get("seed_url")

            if seed_url:
                await run(seed_url)
                return redirect("crawl")

        elif action == "wipe":
            # wipe() is sync ORM → wrap it
            from asgiref.sync import sync_to_async
            await sync_to_async(wipe)()
            return redirect("index")

    return render(request, "index.html")


def crawl(request):
    return render(request, "crawl.html")
