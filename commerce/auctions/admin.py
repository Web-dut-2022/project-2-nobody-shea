from django.contrib import admin
from .models import AuctionsListings, BidRecord, Comments, Watchlist, User

# Register your models here.
admin.site.register(AuctionsListings)
admin.site.register(BidRecord)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(User)