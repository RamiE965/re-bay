from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment, CATEGORY_CHOICES

def index(request):
    return render(request, "auctions/index.html", {
    "Listings": Listing.objects.all(),
    "title": "Active Listings"
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
    
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "startingBid", "image", "category"]

@login_required
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            appendListing = form.save(commit=False)
            appendListing.username = request.user
            appendListing.save()
        return HttpResponseRedirect(reverse("create"))
    else:
        form = ListingForm()
        return render(request, "auctions/create.html", {
            "form": form
        })

class bidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["biddingPrice"]

class commentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]

def listing(request, id):
    try: 
        listing = Listing.objects.get(id=id)
    except:
        return HttpResponse("Error 404: The listing you are searching for does not exist!")

    if listing.ended == True:
        return render(request, "auctions\listing.html", {
            "Listing": listing,
            "ended": True
        })
    return render(request, "auctions\listing.html", {
        "Listing": listing,
        "ended": False,
        "bidForm": bidForm(),
        "commentForm": commentForm()
    })

def listing_close(request, id):
    listing = Listing.objects.get(id=id)
    if request.user == listing.username:
        listing.ended = True
        listing.save()
    
    returnAddress = reverse("listing", kwargs={"id": id})
    return HttpResponseRedirect(returnAddress)

def listing_comment(request, id):
    comment_form = commentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.listing = Listing.objects.get(id=id)
        new_comment.username = request.user
        new_comment.save()
    returnAddress = reverse("listing", kwargs={"id": id})
    return HttpResponseRedirect(returnAddress)

def listing_bid(request, id):
    bid_form = bidForm(request.POST or None)
    if bid_form.is_valid():
        listing = Listing.objects.get(id=id)
        username = request.user
        new_bid = bid_form.save(commit=False)
        current_bids = Bid.objects.filter(listing=listing)
        is_highest_bid = all(new_bid.biddingPrice > n.biddingPrice for n in current_bids)
        is_valid_first_bid = new_bid.biddingPrice >= listing.startingBid

        if is_highest_bid and is_valid_first_bid:
            new_bid.listing = listing
            new_bid.username = request.user
            new_bid.save()

    returnAddress = reverse("listing", kwargs={"id": id})
    return HttpResponseRedirect(returnAddress)

def listing_watch(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        watchlist = request.user.watchlist
        if listing in watchlist.all():
            watchlist.remove(listing)
        else:
            watchlist.add(listing)

    returnAddress = reverse("listing", kwargs={"id": id})
    return HttpResponseRedirect(returnAddress)

def watchlist(request):
    return render(request, "auctions/index.html", {
        "Listings": request.user.watchlist.all(),
        "title": "Watchlist"
    })

CATEGORIES = ["Fashion","Toys","Electronics","Outdoor","Home","Beauty"]

def categories(request):
    return render(request, "auctions/categories.html", {
        "Categories": CATEGORIES
    })

def category(request, name):
    try:
        listing = Listing.objects.filter(
            category=name,
            ended=False
        )
        return render(request, "auctions/index.html", {
            "Listings": listing,
            "title": name
        })
    except:
        return HttpResponse("Something went wrong!")