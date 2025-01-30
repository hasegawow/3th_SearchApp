from django.urls import path
from .views import signup, main, login, artist_search, reset_search

urlpatterns = [
    path('', signup, name='signup'),
    path('login/', login, name='login'),
    path("main/", artist_search, name="search"),
    path('reset/', reset_search, name="reset_search")
]