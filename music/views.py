from django.shortcuts import render, get_object_or_404
from .models import Album

def index(request):
	all_albums = Album.objects.all
	return render(request, 'index.html', {'all_albums': all_albums})

def album(request, album_id):
	album = get_object_or_404(Album, pk=album_id)
	return render(request, 'album.html', {'album': album})	
	

 

