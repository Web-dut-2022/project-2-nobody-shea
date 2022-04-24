from unicodedata import name
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    #re_path(r"^images/(?P<path>.*)/$",serve,{"document_root":settings.MEDIA_ROOT}),
    path("listings/<int:auction_id>/", views.listings, name="listings"),
    path("add_watchlist/<int:auction_id>/", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchList, name="watchlist"),
    path("add_bid/<int:auction_id>/",views.add_bid, name="add_bid"),
    path("add_comment/<int:auction_id>/",views.add_comment, name="add_comment"),
    path("categories",views.categories,name="categories"),
    path("category_listings/<str:category>/",views.category_listings,name="category_listings"),
    path("close_listing/<int:auction_id>",views.close_listing,name="close_listing")

    
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
