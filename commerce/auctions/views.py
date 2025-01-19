from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import CATEGORIES, User, Listing, Bid


class NewListingForm(forms.Form):
    title= forms.CharField(label="Title", max_length=64) 
    description= forms.CharField(label="Description", max_length=255, widget=forms.Textarea()) 
    starting_bid = forms.DecimalField(label="Starting Bid (£)", min_value=0, decimal_places=2, max_digits=6)
    image_url = forms.URLField(label="Image URL (optional)", required=False)
    category = forms.ChoiceField(choices=CATEGORIES, label="Category (optional)", required=False)

class BidForm(forms.Form):
    bid = forms.DecimalField(label="Bid (£)", min_value=0, decimal_places=2, max_digits=6)
    # TODO: validation

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

            listing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, listed_by=request.user)
            listing.save()

            return HttpResponseRedirect(reverse("index"))  # TODO redirect to new listing page

    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })

def listing(request, id):
    listing = Listing.objects.get(id=id)

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_value = form.cleaned_data["bid"]
            new_bid = Bid(listing=listing, bidder=request.user, bid=bid_value)
            new_bid.save()
        
    bids = Bid.objects.filter(listing=id)
    highest_bid = bids.order_by('-bid').first() # returns None if no bids
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(),
        "bids": bids.count(),
        "highest_bid": highest_bid,
    })

def watchlist(request):
    watchlist_listings = Listing.objects.all().filter(watchlist=True)
    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": watchlist_listings,
    })

def watchlist_add(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        listing.watchlist = True
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))

def watchlist_remove(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        listing.watchlist = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))

def categories(request):
     categories = list(CATEGORIES.values())
     categories.remove("")
     return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category):
    category_listings = Listing.objects.all().filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": category_listings,
    })
