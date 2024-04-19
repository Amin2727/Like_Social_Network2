from django.urls import path
from .views import getRoutes
from .views import getRooms, getRoom


urlpatterns = [
    path('', getRoutes),
    path('rooms/', getRooms),
    path('room/<str:pk>/', getRoom),
]
