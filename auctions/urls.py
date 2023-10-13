from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path('listing/<int:listing_id>', views.show, name='show'),
    path('listing/watchlist', views.show_watchlist, name='show_watchlist'),
    path('listing/<int:listing_id>/comment', views.comment, name='comment'),
    path('listing/<int:listing_id>/bid', views.bid, name='bid'),
    path('listing/<int:listing_id>/watchlist', views.watchlist, name='watchlist'),
    path('listing/<int:listing_id>/disbale', views.disbale_listing, name='disable_listing'),
]
