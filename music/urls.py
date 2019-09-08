from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('album/<album_id>', views.album, name='album'),
]