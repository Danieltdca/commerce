from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Listings, Bids, Watchlist, Comments
from .forms import Create_listing, Form, CommentForm


def index(request):
    listings = Listings.objects.all()
    context = {
        "listings": listings,
    }
    return render(request, "auctions/index.html", context)

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

@login_required
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

@login_required
def put_list(request):
    if request.method == "POST":
        form = Create_listing(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            form = Create_listing()
    return render(request, "auctions/create_list.html", {
        "form": Create_listing()
    })
    
def details_listings(request, listingId):
    listing = get_object_or_404(Listings, pk=listingId)
    comments = Comments.objects.filter(comment_list=listing).order_by('-time_stamp')

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.comment_list = listing
            new_comment.save()
            return redirect('listingId', listingId=listing.id)
    else:
        comment_form = CommentForm()

    return render(request, "auctions/details.html", {
        "listing": listing,
        "comments": comments,
        "comment_form": comment_form
    })

        
@login_required
def place_bid(request, listingId):
    if request.method == "POST":
        listing = get_object_or_404(Listings, pk=listingId)

        try:
            bid = float(request.POST["bid_amount"])
        except ValueError:
            messages.error(request, "Invalid bid amount.")
            return redirect("listingId", listingId=listingId)

        if bid <= float(listing.amount):
            messages.error(request, "Your bid must be higher than the current price.")
            return redirect("listingId", listingId=listingId)

        # Save the valid bid
        new_bid = Bids(
            bid_amount=bid,
            user=request.user,
            bid_list=listing
        )
        new_bid.save()

        # Update listing's current amount
        listing.amount = bid
        listing.save()

        messages.success(request, "Bid placed successfully!")
        return redirect("listingId", listingId=listingId)
    
@login_required
def toggle_watchlist(request, listingId):
    listing = get_object_or_404(Listings, pk=listingId)

    # Check if it's already in the user's watchlist
    watch_item = Watchlist.objects.filter(user=request.user, listing=listing).first()

    if watch_item:
        watch_item.delete()
    else:
        Watchlist.objects.create(user=request.user, listing=listing)

    return redirect("listingId", listingId=listing.id)

@login_required
def watchlist(request):
    watch_items = Watchlist.objects.filter(user=request.user)
    listings = [item.listing for item in watch_items if item.listing]
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
    
@login_required
def close_auction(request, listingId):
    listing = get_object_or_404(Listings, pk=listingId)
    if request.user != listing.owner:
        messages.error(request, "You are not Athorized to close this auction.")
        return redirect("listingId", listingId=listing.id)
    
    highest_bid = Bids.objects.filter(bid_list=listing).order_by("-bid_amount").first()
    if highest_bid:
        listing.winner = highest_bid.user
    
    listing.active = False
    listing.save()
    
    messages.success(request, "Auction Closed successfully.")
    return redirect("listingId", listingId=listing.id)