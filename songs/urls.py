from django.urls import path, include
from rest_framework.routers import DefaultRouter

from artists.views import AlbumSongViewSet

from .views import (
    GenreViewSet,
    PlaylistSongViewSet,
    PlaylistViewSet,
    RatingViewSet,
    SongViewSet,
)


router = DefaultRouter()

router.register(r"genres", GenreViewSet)
router.register(r"songs", SongViewSet)
router.register(r"ratings", RatingViewSet)
router.register(r"playlists", PlaylistViewSet, basename="playlist-songs-all")
router.register(
    r"users/(?P<user_id>[^/.]+)/playlists", PlaylistViewSet, basename="playlist-songs"
)
router.register(
    r"playlists/(?P<playlist_id>[^/.]+)/songs",
    PlaylistSongViewSet,
    basename="playlist-songs",
)


urlpatterns = [
    path("", include(router.urls)),
]
