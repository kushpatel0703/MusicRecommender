from django.contrib import admin
from .models import Artist, Album, ArtistTag, AlbumTag
# Register your models here.
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(ArtistTag)
admin.site.register(AlbumTag)