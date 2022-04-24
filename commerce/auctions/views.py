from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import CharField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Watchlist, AuctionsListings,BidRecord,Comments

LISTING_CATEGORIES = [
    ('BOOKS', 'Books'),
    ('CLOTHING','Clothing'),
    ('TOOLS','Tools'),
    ('CHEMICALS','Chemicals'),
    ('FOOD','Food'),
    ('ARTWORK','Artwork'),
    ('HEALTH', 'Health'),
    ('OTHER','other')
]

def index(request):
    data = AuctionsListings.objects.filter(active = True)
    if request.user.is_authenticated:
        watch = Watchlist.objects.all().filter(uid=request.user).count()
    else:
        watch = False
    return render(request, "auctions/index.html", {
        "data":data,
        "watchlist":watch,
        "Active":"Active"
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


@login_required
def create_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image')
        imgURL = '/images/'+image.name
        startingBid = request.POST['startingBid']
        user = User.objects.get(id = request.user.id)
        auction_listing = AuctionsListings(title=title, description=description, price=startingBid, image = image, imgURL=imgURL, active = True, category = "Other")
        auction_listing.uid = user
        auction_listing.save()
        return redirect('/')
    else:
        return render(request, "auctions/create.html")


def listings(request, auction_id):
    data = AuctionsListings.objects.filter(id = auction_id)
    comments = Comments.objects.filter(aid = auction_id)
    if request.user.is_authenticated:
        added = Watchlist.objects.filter(uid=request.user, aid=auction_id)
        if request.user == data[0].uid:
            creator = True
        else:
            creator = False
    else:
        added = False
        creator = False
    return render (request, "auctions/detail.html", {
        "data": data[0],
        "added": added,
        "creator":creator,
        "comments":comments
        })


@login_required
def add_watchlist(request, auction_id):
    listing = AuctionsListings.objects.get(id = auction_id)
    added = Watchlist.objects.filter(uid = request.user, aid = listing)
    if added:
        added.delete()
        return HttpResponseRedirect(reverse("listings", args=(auction_id,)))
    else:
        add = Watchlist(uid = request.user, aid = listing)
        add.save()
        return HttpResponseRedirect(reverse("listings", args=(listing.id,)))


@login_required
def watchList(request):
    watch = Watchlist.objects.all().filter(uid = request.user).values()
    items = []
    for item in watch.iterator():
        items.append(item['aid_id'])
    data = AuctionsListings.objects.all().filter(id__in = items)
    return render(request, "auctions/index.html", {
        "data": data,
        "Active":""
        })


@csrf_exempt
def add_bid(request, auction_id):
    current_bid = AuctionsListings.objects.get(id=auction_id)
    current_bid = current_bid.price

    if request.method == "POST":
        user_bid = float(request.POST.get("price"))
        if user_bid > current_bid:
            listing_items = AuctionsListings.objects.get(id=auction_id)
            listing_items.price = user_bid  
            listing_items.save()

            Bid_exist = BidRecord.objects.filter(aid=listing_items)
            if Bid_exist:
                Bid_exist.bid = user_bid
                Bid_exist.uid = request.user
                BidRecord.objects.filter(aid=listing_items).update(uid=request.user, bid=user_bid)
            else:
                Bid = BidRecord(aid=listing_items, uid=request.user, bid=user_bid)
                Bid.save()
            return listings(request, auction_id)
        else:
            return HttpResponseRedirect(reverse("index"))  


@csrf_exempt
def add_comment(request, auction_id):
    listing = AuctionsListings.objects.get(id=auction_id)
    comments = Comments.objects.filter(aid=listing)

    if request.method == "POST":
        content = request.POST.get('content')
        comment = Comments(aid=listing, uid=request.user, content=content) 
        comment.save()  
        return HttpResponseRedirect(reverse("listings", args=(auction_id,)))
    else:
        return render(request, "auctions/detail.html", {
            "data": listings,
            "comments": comments,
        })


def categories(request):
    categories = AuctionsListings.objects.filter(active=True).order_by("category").values_list("category", flat=True).distinct()
    categories = [category.capitalize() for category in categories if category is not None]
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_listings(request, category):
    list = AuctionsListings.objects.filter(category=category.upper()).filter(active=True)
    property(list)
    return render(request, "auctions/index.html", {
        "listings": list
    })


@login_required
def close_listing(request, auction_id):
    close = AuctionsListings.objects.get(uid=request.user, id=auction_id)
    close.active = False
    close.save()
    bidder = BidRecord.objects.get(aid = close)

    if bidder:
        winner = bidder.uid
        return render(request, "auctions/detail.html", {
            "data": close,
            "winner": winner
        })
    else:
        return HttpResponseRedirect(reverse("index"))