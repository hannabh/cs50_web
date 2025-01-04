import markdown2
import random

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms

from . import util

class NewEntryForm(forms.Form):
    page_title= forms.CharField(label="Page title") 
    page_content = forms.CharField(widget=forms.Textarea, label="Page content in Markdown format")

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

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)  # Save the data submitted by the user as a form
        if form.is_valid():
            page_title = form.cleaned_data["page_title"]
            if page_title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "page_title": page_title
                })
            else:
                page_content = form.cleaned_data["page_content"]
                with open(f'./entries/{page_title}.md', 'w') as file:  # Save to disk
                    file.write(page_content)
                return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": page_title}))

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })

def error(request, page_title):
    return HttpResponseRedirect(reverse("wiki:error", kwargs={"page_title": page_title}))

def random_page(request):
    entries = util.list_entries()
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": random.choice(entries)}))
