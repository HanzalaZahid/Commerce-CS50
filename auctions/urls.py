from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('listing/<str:listing_id>', views.show, name='show'),
    path('listing/<str:listing_id>/comment', views.comment, name='comment'),
    path('listing/<str:listing_id>/bid', views.bid, name='bid'),
    path('listing/<str:listing_id>/watchlist', views.watchlist, name='watchlist'),
]
