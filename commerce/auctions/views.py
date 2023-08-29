from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime

from .models import User, Category, Listing, Comments, Bid




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
    
def test(request):
    activeListings = Listing.objects.filter(active=True)
    return render(request, "auctions/test.html",{
        'listings':activeListings

    })

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

def index(request):
    activeListings = Listing.objects.filter(active=True)
    owner = request.user
    inWatchlist = 0
    if request.user.is_authenticated:
        listings = owner.watchlistUser.all()
        for x in listings:
            inWatchlist += 1
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        'listings':activeListings,
        'categories': categories,
        "inWatchlist":inWatchlist

    })

def addListing(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        inWatchlist = 0
        listings = request.user.watchlistUser.all()
        for x in listings:
            inWatchlist += 1
        return render(request, 'auctions/addListing.html', {
            'categories': categories,
            "inWatchlist":inWatchlist,
            
        })
    else:
        owner = request.user
        title = request.POST['title']
        description = request.POST['description']
        imgURL = request.POST['imgURL']
        price = request.POST['price']
        category = request.POST['category']
        categoryData = Category.objects.get(categoryType=category)
        bid =Bid(bid=int(price), user= owner)
        bid.save()

        

        newListing = Listing(title=title, description=description, imgURL=imgURL, price=bid, category=categoryData, owner=owner )
        newListing.save()

        return HttpResponseRedirect(reverse('index'))
         
def categorize(request):
    if request.method =="POST":
        categorizeBy = request.POST['category']
        category = Category.objects.get(categoryType = categorizeBy)
        activeListings = Listing.objects.filter(active=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/categorize.html",{
            'listings':activeListings,
            'categories': categories

    })
def listing(request, id):
    listingDetails = Listing.objects.get(pk=id)
    color = 0 
    if listingDetails.category.categoryType == "Fire":
        color = "#fd7d24"
    elif listingDetails.category.categoryType == "Water":
        color = "#4592c4"
    elif listingDetails.category.categoryType == "Grass":
        color = "#9bcc50"
    elif listingDetails.category.categoryType == "Flying":
        color = "#3dc7ef"
    elif listingDetails.category.categoryType == "Electric":
        color = "#eed535"
    elif listingDetails.category.categoryType == "Ghost":
        color = "#7b62a3"
    elif listingDetails.category.categoryType == "Poison":
        color = "#b97fc9"
   
    watchlisted = request.user in listingDetails.watchlist.all()
    comments = Comments.objects.filter(listing=listingDetails)
    owner = request.user.username == listingDetails.owner.username
    status = ""
    if listingDetails.active == False:
        status = "Archived"
    else:
        status = datetime.datetime.now().strftime(" on %B %d, %Y")
       # formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    inWatchlist = 0
    listings = request.user.watchlistUser.all()
    for x in listings:
        inWatchlist += 1
    #highest bid calc 
    
    return render(request, "auctions/listing.html",{
        "listing":listingDetails,
        "watchlist":watchlisted,
        "comments":comments,
        "inWatchlist":inWatchlist,
        "color":color,
        "owner":owner,
        "status": status
    })
def watchlist(request):
    user = request.user
    listings = user.watchlistUser.all()
    inWatchlist = 0
    listings = user.watchlistUser.all()
    for x in listings:
        inWatchlist += 1
    return render(request, "auctions/watchlist.html",{
        "listings":listings,
        "inWatchlist":inWatchlist
    })
    

def addBid(request,id):
    newBid = request.POST['newBid']
    listingDetails = Listing.objects.get(pk=id)
    watchlisted = request.user in listingDetails.watchlist.all()
    comments = Comments.objects.filter(listing=listingDetails)
    owner = request.user.username == listingDetails.owner.username
    color = 0 
    if listingDetails.category.categoryType == "Fire":
        color = "#fd7d24"
    elif listingDetails.category.categoryType == "Water":
        color = "#4592c4"
    elif listingDetails.category.categoryType == "Grass":
        color = "#9bcc50"
    elif listingDetails.category.categoryType == "Flying":
        color = "#3dc7ef"
    elif listingDetails.category.categoryType == "Electric":
        color = "#eed535"
    elif listingDetails.category.categoryType == "Ghost":
        color = "#7b62a3"
    elif listingDetails.category.categoryType == "Poison":
        color = "#b97fc9"
    if int(newBid) > listingDetails.price.bid:
        updatedBid = Bid(user=request.user, bid=int(newBid))
        updatedBid.save()
        listingDetails.price =updatedBid
        listingDetails.save()
        return render(request, "auctions/listing.html",{
        "listing":listingDetails,
        "watchlist":watchlisted,
        "comments":comments,
        "owner":owner,
        "message": "Success",
        "color":color,
        "update": True
    })
    else:
        return render(request, "auctions/listing.html",{
        "listing":listingDetails,
         "watchlist":watchlisted,
        "comments":comments,
        "owner":owner,
        "message": "Failed! Bid is lower than price!",
        "color":color,
        "update": False
    })
    
def close(request, id):
    listingDetails = Listing.objects.get(pk=id)
    listingDetails.active =False
    listingDetails.save()
    watchlisted = request.user in listingDetails.watchlist.all()
    comments = Comments.objects.filter(listing=listingDetails)
    owner = request.user.username == listingDetails.owner.username
    return render(request, "auctions/listing.html",{
        "watchlist":watchlisted,
        "comments":comments,
        "listing":listingDetails,
        "owner":owner,
        "update": True
    })


def removeWatchlist(request, id):
    status = Listing.objects.get(pk=id)
    user = request.user
    status.watchlist.remove(user)
    return HttpResponseRedirect(reverse('listing' , args=(id, )))
def addWatchlist(request, id):
    status = Listing.objects.get(pk=id)
    user = request.user
    status.watchlist.add(user)
    return HttpResponseRedirect(reverse('listing' , args=(id, )))

def addComment(request,id):
    user = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST["newComment"]
    newComment = Comments(commenter=user, listing=listingData, message=message)
    newComment.save()
    return HttpResponseRedirect(reverse('listing' , args=(id, )))
    