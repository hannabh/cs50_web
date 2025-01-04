import markdown2
import random

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    content = util.get_entry(title)
    if content != None:
        content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content,
    })

def search(request):
    query = request.GET['q']
    entries = util.list_entries()
    if query in entries:
        return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": query}))
    else:
        search_results = [title for title in entries if query.lower() in title.lower()]
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "search_results": search_results
        })
    
def random_page(request):
    entries = util.list_entries()
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": random.choice(entries)}))
