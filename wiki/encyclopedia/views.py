import markdown2
import random

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms

from . import util

class NewEntryForm(forms.Form):
    title= forms.CharField(label="Page title") 
    content = forms.CharField(widget=forms.Textarea, label="Page content in Markdown format")

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Page content in Markdown format")

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
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "title": title
                })
            else:
                content = form.cleaned_data["content"]
                with open(f'./entries/{title}.md', 'w') as file:  # Save to disk
                    file.write(content)
                return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": title}))

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })

def error(request, title):
    return HttpResponseRedirect(reverse("wiki:error", kwargs={"title": title}))

def edit(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            with open(f'./entries/{title}.md', 'w') as file:
                file.write(content)
            return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": title}))
    
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditEntryForm(initial={"content": content}),
    })

def random_page(request):
    entries = util.list_entries()
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": random.choice(entries)}))
