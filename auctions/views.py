# from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from .forms import ListingForm, BidForm
from .models import User
# import copy

@login_required
def create(request):
    
    if request.method == "POST":
        
        listing_form_filled = ListingForm(data=request.POST)
     
        if listing_form_filled.is_valid():
            
            new_listing = listing_form_filled.save()
            listing_id = new_listing.pk
            return HttpResponseRedirect(reverse("add_to_watchlist", args=[listing_id]))

        return render(request, "auctions/create.html",{
            "listing_form":listing_form_filled
        })
    
    
    return render(request, "auctions/create.html", {
        "listing_form": ListingForm(initial={"seller":request.user.id})
    })

@login_required
def watchlist(request):
    listings = Listing.objects.filter(followers=request.user.id).all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "watchlist":True,
    })



@login_required
def add_to_watchlist(request, listing_id):
    listing_id = int(listing_id)
    user = User.objects.get(pk=request.user.id)
    user.favorites.add(listing_id)

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


# listing_remove_from_watchlist
@login_required
def remove_from_watchlist(request):
  
    user = User.objects.get(pk=request.user.id)
    favorite_id = int(request.POST["favorite_id"])
    user.favorites.remove(favorite_id)    

    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def in_listing_remove_to_watchlist(request):
  
    user = User.objects.get(pk=request.user.id)
    favorite_id = int(request.POST["favorite_id"])
    user.favorites.remove(favorite_id)    

    return HttpResponseRedirect(reverse("listing", args=[favorite_id]))



@login_required
def add_comment(request):
    user = User.objects.get(pk=request.user.id)
    listing_id = int(request.POST["listing_id"])
    listing = Listing.objects.get(pk=int(listing_id))
    commentary = request.POST["commentary"]
    
    comment = Comment(message=commentary, user=user, listing=listing)
    comment.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required
def remove_comment(request):
    comment_id = request.POST["comment_id"]
    listing_id = int(request.POST["listing_id"])
    comment = Comment.objects.get(pk=int(comment_id))
    comment.delete()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def index(request):
    listings = Listing.objects.all()
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
    
        return render(request, "auctions/index.html",
        {
            "user":user,
            "listings":listings
        })
    else:
        return render(request, "auctions/index.html",
        {
            "listings":listings
        })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories":categories,
    })

def category(request, category_value):

    category = Category.objects.get(pk=category_value)
    if category is None:
        return render(request, "auctions/category.html", {
        "title":"Invalid Category",
    })

    listings = Listing.objects.filter(category=category).all()
    
    return render(request, "auctions/category.html", {
        "listings":listings,
        "title":category.category,
    })
   

def listing(request, listing_id):

    # For show a helper message outside of the forms
    message = False
    best_bid = False
    
    # POST METHOD IS FOR MANAGE BID CREATION
    if request.method == "POST":
        
        # filling the form with data
        bid_form = BidForm(data=request.POST)

        # checking if data-form is complete
        if bid_form.is_valid():
            listing_id = int(bid_form.cleaned_data["listing"])
            offerent_id = int(bid_form.cleaned_data["offerent"])
            price = int(bid_form.cleaned_data["price"])

            # creating a Bid object
            listing = Listing.objects.get(pk=listing_id)
            offerent = User.objects.get(pk=offerent_id)

            bid = Bid(price=price, listing=listing, offerent=offerent)

            # checking if the price of bid is valid
            try:
                bid.clean()

            # if not, pass and change messages to True
            except ValidationError:
                message = True

            # if all it's OK
            else:
                bid.save()
                # add to watchlist, and watchlist redirect to this view in GET method
                return HttpResponseRedirect(reverse("add_to_watchlist", args=[listing_id]))


    # GET METHOD
    listing = Listing.objects.get(pk=int(listing_id))
    
    # when the listing required exist
    if listing is not None:

        # get all the comments for this listing
        comments = listing.comment.all()

        if request.user.is_authenticated:
            
            # get the minimum price valid
            best_bid = Bid.objects.filter(listing=listing_id).order_by("-price").first()
            if best_bid:        
                price = best_bid.price + 1
            else:
                price = listing.price
            

            # message for reprompt
            if message:
                message = f"Your bid price must be almost of {price}"

            # cretaing a BID form an initialize with the minimum valid price, and other data
            bid_form = BidForm(
                initial={
                    "listing":listing_id,
                    "offerent":request.user.id,
                    "price":price
                })

            # getting the favorites of this user
            user = User.objects.get(pk=int(request.user.id))
            favorite = user.favorites.filter(pk=listing_id).first()
            
        
        # When the user is not logged
        else:
            bid_form = False
            favorite = False

        return render(request, "auctions/listing.html",{
            "listing":listing,
            "comments":comments,
            "bid_form":bid_form,
            "message":message,
            "favorite":favorite,
            "best_bid":best_bid,
        })

    # when the listing required doesn't exist
    else:
        return render(request, "auctions/index.html",{
            "message":"Product Not Found"
        })
@login_required        
def close_listing(request):
    if request.method == "POST":
        listing_id = int(request.POST["listing_id"])
        listing = Listing.objects.get(pk=listing_id)
        if listing:
            listing.active = False
            listing.save()
 
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

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
