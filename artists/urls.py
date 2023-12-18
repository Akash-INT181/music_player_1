from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AlbumSongViewSet,
    AlbumViewSet,
    ArtistSongViewSet,
    ArtistViewSet,
    create_album,
)


router = DefaultRouter()

router.register(r"artists", ArtistViewSet)
router.register(r"albums", AlbumViewSet)
router.register(
    r"albums/(?P<album_id>[^/.]+)/songs", AlbumSongViewSet, basename="album-songs"
)
router.register(
    r"artists/(?P<artist_id>[^/.]+)/songs", ArtistSongViewSet, basename="artist-songs"
)
urlpatterns = [
    path("", include(router.urls)),
    path("putdata/", view=create_album, name="create_album"),
]
