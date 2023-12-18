from django.contrib import admin

from .models import Genre, Playlist, Rating, Song

# Register your models here.
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Genre)
admin.site.register(Rating)
