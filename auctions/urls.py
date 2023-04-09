from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("create/", views.create, name="create"),
    path("watchlist/", views.watchlist, name="watchlist"),
    # hice un cambio en add
    path("watchlist/add/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("listing/watchlist/remove", views.in_listing_remove_to_watchlist, name="in_listing_remove_to_watchlist"),
    path("commentary/add", views.add_comment, name="add_comment"),
    path("commentary/remove", views.remove_comment, name="remove_comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_value>", views.category, name="category"),
    path("listing/close", views.close_listing, name="close_listing"),
    

]
