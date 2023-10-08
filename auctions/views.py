from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import *
from .models import User


# FORMS GOES HERE
class BidForm(forms.Form):
    def __init__(self, listing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        highest_bid = Bid.objects.filter(listing = listing).order_by('-price').first()
        highest_bid_price = highest_bid.price + 1 if highest_bid else 1
        self.fields['price'] = forms.DecimalField(label = 'Price', min_value=highest_bid_price)


# VIEWS GOES HERE
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings'   :   listings,
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


def show(request, listing_id):
    try:
        listing = Listing.objects.get(id = listing_id)
    except Listing.DoesNotExist:
        return render(request, 'auctions/error.html', {
            'message' : '404 - Listing Not Found'
        })
    
    bid_form = BidForm(listing=listing)
    comments = Comment.objects.filter(listing = listing_id)
    highestbid = Bid.objects.filter(listing = listing).order_by('-price').first()
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    existing_watchlist = Watchlist.objects.filter(user = user, listing = listing)
    return render(request, 'auctions/show.html', {
        'listing' : listing,
        'comments' : comments,
        'bid_form' : bid_form,
        'highestbid' : highestbid.price if highestbid else None,
        'watchlist' : existing_watchlist if existing_watchlist.exists() else None
    })

def bid(request, listing_id):
    if request.method == 'POST':
        amount = request.POST.get('price')
        user = User.objects.get(id = request.user.id)
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return render(request, 'auctions/error.html', {
                'msg' : 'Listing Does Not Exists'
            })
        existing_bid = Bid.objects.filter(user = user, listing = listing)
        if not existing_bid.exists():
            bid = Bid(user = user, price = amount, listing = listing)
            bid.save()
            return HttpResponseRedirect(reverse('show', args=[listing_id]))
        else:
            messages.error(request, 'You\'ve already bided on this Listing')
            return HttpResponseRedirect(reverse('show', args=[listing_id]))
    return render(request, 'auctions/error.html', {
        'message' : 'Not Allowed'
    })
           

def comment(request, listing_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id = user_id)
        comment = request.POST.get('comment')
        listing = Listing.objects.get(id = listing_id)
        new_comment = Comment(user = user, comment = comment, listing = listing)
        new_comment.save()
        messages.success(request, 'Comment Added Successfully')
        return HttpResponseRedirect(reverse('show', args=[listing_id]))
    return HttpResponse(f'Comment for { listing_id}')

def watchlist(request, listing_id):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(id = user_id)
        listing = Listing.objects.get(id = listing_id)
        existing_watchlist = Watchlist.objects.filter(user = user, listing = listing)
        if existing_watchlist.exists():
            existing_watchlist.delete()
            messages.success(request, 'Item Removed From Watchlist')
        else:
            new_item = Watchlist(user = user, listing = listing)
            new_item.save()
            messages.success(request, 'Item Added To Watchlist')
        return HttpResponseRedirect(reverse('show', args=[listing_id]))
    else:
        return render(request, 'auctions/error.html', {
            'message' : 'Not Allowed'
        })