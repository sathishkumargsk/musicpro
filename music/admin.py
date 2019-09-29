from import_export import fields, resources, widgets
from import_export.widgets import ForeignKeyWidget
from django.contrib import admin
from .models import Artist, Album, Song
from urllib import request
from django.conf import settings
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin, ImportExportMixin
from django.db import IntegrityError
import pprint
import logging
import os
import eyed3


media_folder = "media/"
"""
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

"""

def before_import_row(self,row, **kwargs):
    if 'song_file' in row :
        mp3file = row['song_file']
        mp3filename = mp3file.rsplit('/', 1)
        filename = row['song_title']
        sitename = "Newtamilsongs.In"
        extension = ".mp3"
        newfilename = filename+"-"+sitename+extension
        mp3filepath = media_folder+mp3file
        new_song_file = "mp3/"+newfilename
        newfilenamepath = media_folder+"mp3/"+newfilename
        coverimage = Album.objects.get(album_title=row['album'])
        albumcover = coverimage.album_cover_image.url;
        albumcoverpath = albumcover[1:]
        if os.path.isfile(mp3filepath):
            mp3filepathchecked = mp3filepath
        else:
            mp3filepathchecked = newfilenamepath
        audiofile  = eyed3.load(mp3filepathchecked)
        audiofile.tag.title = row['song_title']
        audiofile.tag.artist = row['artist']
        audiofile.tag.album = row['album']
        audiofile.tag.images.remove('')
        imagedata = open(albumcoverpath,"rb").read()
        # append image to tags
        audiofile.tag.images.set(3,imagedata,"image/jpeg")
        audiofile.tag.save()
        if os.path.isfile(mp3filepath):
            os.rename(mp3filepath,newfilenamepath)
        row['song_file'] = new_song_file # update value to id ob new object

resources.Resource.before_import_row = before_import_row


class ArtistResource(resources.ModelResource):
    class Meta:
        model = Artist
        skip_unchanged = True
        report_skipped = True

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        try:
            super(ArtistResource, self).save_instance(instance, using_transactions, dry_run)
        except IntegrityError:
            pass

class ArtistAdmin(ImportExportModelAdmin):
    resource_class = ArtistResource

class AlbumResource(resources.ModelResource):
    artist = fields.Field(
        column_name='artist',
        attribute='artist',
        widget=ForeignKeyWidget(Artist, 'artist_name'))
    class Meta:
        model = Album
        skip_unchanged = True
        report_skipped = True
    def save_instance(self, instance, using_transactions=True, dry_run=False):
        try:
            super(AlbumResource, self).save_instance(instance, using_transactions, dry_run)
        except IntegrityError:
            pass

class AlbumAdmin(ImportExportModelAdmin):
    resource_class = AlbumResource

class SongResource(resources.ModelResource):
    album = fields.Field(
        column_name='album',
        attribute='album',
        widget=ForeignKeyWidget(Album, 'album_title'))
    artist = fields.Field(
        column_name='artist',
        attribute='artist',
        widget=ForeignKeyWidget(Artist, 'artist_name'))
    song_file = fields.Field(attribute='song_file', column_name='song_file')
    class Meta:
        model = Song
        skip_unchanged = True
        report_skipped = True
    def save_instance(self, instance, using_transactions=True, dry_run=False):
        try:
            super(SongResource, self).save_instance(instance, using_transactions, dry_run)
        except IntegrityError:
            pass


class SongAdmin(ImportExportModelAdmin):
    resource_class = SongResource

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
