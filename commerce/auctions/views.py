from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import CATEGORIES, User, Listing


class NewListingForm(forms.Form):
    title= forms.CharField(label="Title", max_length=64) 
    description= forms.CharField(label="Description", max_length=255, widget=forms.Textarea()) 
    starting_bid = forms.DecimalField(label="Starting Bid (£)", min_value=0, decimal_places=2, max_digits=6)
    image_url = forms.URLField(label="Image URL (optional)", required=False)
    category = forms.ChoiceField(choices=CATEGORIES, label="Category (optional)", required=False)


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]

            listing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category)
            listing.save()

            return HttpResponseRedirect(reverse("index"))  # TODO redirect to new listing page

    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })

def listing(request, id):
    listing = Listing.objects.get(id=id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
    })
