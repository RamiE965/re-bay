from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.category, name="category"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("listing/<str:id>/end", views.listing_close, name="listing_close"),
    path("listing/<str:id>/comment", views.listing_comment, name="listing_comment"),
    path("listing/<str:id>/bid", views.listing_bid, name="listing_bid"),
    path("auction/<str:id>/watch", views.listing_watch, name="listing_watch")
]
