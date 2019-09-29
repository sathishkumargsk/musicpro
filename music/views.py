import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Album

def index(request):
	all_albums = Album.objects.all
	return render(request, 'index.html', {'all_albums': all_albums})

def album(request, album_title):
	album = get_object_or_404(Album, album_title=album_title)
	return render(request, 'album.html', {'album': album})
