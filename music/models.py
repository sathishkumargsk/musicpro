from django.db import models

class Artist(models.Model):
	artist_name = models.CharField(max_length=250)

	def __str__(self):
		return self.artist_name

class Album(models.Model):
	artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
	album_title = models.CharField(max_length=250)
	genre = models.CharField(max_length=100)
	album_cover_image = models.FileField()

	def __str__(self):
		return self.album_title

class Song(models.Model):
	artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	song_title = models.CharField(max_length=250)
	song_file = models.FileField()

	def __str__(self):
		return self.song_title 

		

