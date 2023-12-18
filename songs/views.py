from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import (
    AllDisplayPlaylist,
    GenreSerializer,
    PlaylistPostSerializer,
    PlaylistSerializer,
    PlaylistSongSerializer,
    RatingSerializer,
    SongSerializer,
)

from .models import Genre, Playlist, Rating, Song
from django.contrib.postgres.search import SearchVector, SearchQuery


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # filter_backends = [
    #     "django_filters.rest_framework",
    #     "rest_framework.search.SearchFilter",
    # ]
    # search_fields = [
    #     "song_name",
    #     "genre__genre_name",
    #     "album__album_name",
    #     "album__artist__artist_name",
    # ]

    @action(detail=False, methods=["get"])
    def search_songs(self, request):
        query = request.query_params.get("q", None)

        if not query:
            return Response(
                {"error": 'Missing search query parameter "q"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Perform full-text search
        songs = (
            Song.objects.annotate(
                rank=SearchVector("song_name", weight="A")
                + SearchVector("genre__genre_name", weight="A")
                + SearchVector("album__album_name", weight="A")
                + SearchVector("album__artist__artist_name", weight="A")
            )
            .filter(rank=SearchQuery(query))
            .order_by("-rank")
        )

        serializer = self.get_serializer(songs, many=True)
        return Response(serializer.data)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    # serializer_class = PlaylistSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return playlists that belong to the authenticated user
        # print(Playlist.objects.filter(user=self.request.user))
        return Playlist.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        # Use different serializers for different HTTP methods
        if self.request.method == "GET":
            return AllDisplayPlaylist
        elif self.request.method == "POST":
            return PlaylistPostSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return PlaylistSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Ensure that only the owner can update
        if instance.user != request.user:
            response_data = {
                "detail": "You do not have permission to perform this action."
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        # Ensure that only the owner can perform updates
        instance = serializer.instance
        # print(serializer.validated_data)
        if instance.user != serializer.validated_data.get("user"):
            response_data = {
                "detail": "You do not have permission to perform this action."
            }
            raise PermissionError(response_data)

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Ensure that only the owner can delete
        if instance.user != request.user:
            response_data = {
                "detail": "You do not have permission to perform this action."
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class PlaylistSongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSongSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        playlist_id = self.kwargs.get("playlist_id")
        return Playlist.objects.filter(id=playlist_id, user=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
