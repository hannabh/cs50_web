from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Post

class NewPostForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea)

def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all().order_by('-datetime')
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    # For POST requests, submit the form
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = Post(user=request.user, content=form.cleaned_data["content"])
            post.save()
        
            return render(request, "network/index.html", {
                 "posts": Post.objects.all().order_by('-datetime')
            })

    else:
        # For GET requests, create a new form
        form = NewPostForm()
        return render(request, "network/new_post.html", {
            "form": form,
        })

def profile(request, username):
    user = User.objects.get(username=username)
    if user in request.user.profiles_following.all():
        is_following = True
    else:
        is_following = False

    return render(request, "network/profile.html", {
        "username": user.username,
        "followers": user.followers.all(),
        "following": user.profiles_following.all(),
        "is_following": is_following,
        "posts": Post.objects.filter(user=user).order_by('-datetime'),
    })

def follow(request, username):
    if request.method == "POST":
        user = User.objects.get(username=username)
        request.user.profiles_following.add(user)
        request.user.save()  # needed?
    return render(request, "network/profile.html", {
        "username": user.username,
        "followers": user.followers.all(),
        "following": user.profiles_following.all(),
        "is_following": True,
        "posts": Post.objects.filter(user=user).order_by('-datetime'),
    })

def unfollow(request, username):
    if request.method == "POST":
        user = User.objects.get(username=username)
        request.user.profiles_following.remove(user)
        request.user.save()  # needed?
    return render(request, "network/profile.html", {
        "username": user.username,
        "followers": user.followers.all(),
        "following": user.profiles_following.all(),
        "is_following": False,
        "posts": Post.objects.filter(user=user).order_by('-datetime'),
    })
