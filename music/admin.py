from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from django.contrib import admin
from .models import Artist, Album, Song
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin, ImportExportMixin


class ArtistResource(resources.ModelResource):
    class Meta:
        model = Artist

class ArtistAdmin(ImportExportModelAdmin):
    resource_class = ArtistResource

class AlbumResource(resources.ModelResource):
    artist = fields.Field(
        column_name='artist',
        attribute='artist',
        widget=ForeignKeyWidget(Artist, 'artist_name'))
    class Meta:
        model = Album

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

class SongAdmin(ImportExportModelAdmin):
    resource_class = SongResource

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
