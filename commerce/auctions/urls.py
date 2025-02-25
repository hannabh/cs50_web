from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:id>/watchlist_add", views.watchlist_add, name="watchlist_add"),
    path("listing/<int:id>/watchlist_remove", views.watchlist_remove, name="watchlist_remove"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_listings, name="category_listings"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
]