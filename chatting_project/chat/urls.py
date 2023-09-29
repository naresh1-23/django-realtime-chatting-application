from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainHome, name = 'home'),
    path("check-room/<int:pk>/", views.CheckRoom, name = 'check-room'),
    path("<int:pk>/", views.home, name = 'chat-home'),
    path("search/<q>/", views.Search, name = 'search')
]
