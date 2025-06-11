from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list", views.put_list, name="create_list"),
    path("<int:listingId>", views.details_listings, name="listingId"),
    path("bid/<int:listingId>", views.place_bid, name="place_bid"),
    path("<int:listingId>/watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("close/<int:listingId>/", views.close_auction, name="close_auction"),

]
