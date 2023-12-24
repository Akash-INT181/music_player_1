from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AlbumSongViewSet,
    AlbumViewSet,
    ArtistRegisterViewSet,
    ArtistSongViewSet,
    ArtistViewSet,
    CustomTokenObtainPairView,
    create_album,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
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
    path(
        "registerartists/",
        view=ArtistRegisterViewSet.as_view(),
        name="artist_register",
    ),
    path("", include(router.urls)),
    path("putdata/", view=create_album, name="create_album"),
    path(
        "artist/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("artist/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
