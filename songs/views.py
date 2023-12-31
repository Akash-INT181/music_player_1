from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action

from artists.views import CustomJWTAuthentication, HasAnyPermissions
from songs.document import SongDocument
from django_elasticsearch_dsl_drf.pagination import QueryFriendlyPageNumberPagination

from .serializers import (
    AllDisplayPlaylist,
    GenreSerializer,
    PlaylistPostSerializer,
    PlaylistSerializer,
    PlaylistSongSerializer,
    RatingSerializer,
    SongDocumentSerializer,
    SongSerializer,
)

from .models import Genre, Playlist, Rating, Song

# from elasticconnect.elastic_search_config import es, SONG_INDEX_NAME

from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    FilteringFilterBackend,
    SuggesterFilterBackend,
    MultiMatchSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.played += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search_songs(self, request):
        query = request.query_params.get("q", None)

        if not query:
            return Response(
                {"error": 'Missing search query parameter "q"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # data = es.search(index=SONG_INDEX_NAME, q="*" + query + "*", size=100)
        # search = []

        # for item in data["hits"]["hits"]:
        #     item1 = item["_source"]
        #     item1["_score"] = item["_score"]
        #     # data = {}
        #     # for key, val in item1.items():
        #     #     if key == "id":
        #     #         data[key] = val
        #     #     elif key == "album":
        #     #         data[key + "_id"] = val["id"]
        #     #         data[key] = val["title"]
        #     #         data["artist_id"] = val["artist"]["id"]
        #     #         data["artist_name"] = val["artist"]["name"]
        #     #     elif key == "genre":
        #     #         data[key + "_id"] = val["id"]
        #     #         data[key + "_name"] = val["name"]
        #     #     else:
        #     #         data[key] = val
        #     search.append(item1)
        # # print(data)
        # return Response(search)


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
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasAnyPermissions]


class SongDocumentView(DocumentViewSet):
    document = SongDocument
    serializer_class = SongDocumentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
        SuggesterFilterBackend,
        MultiMatchSearchFilterBackend,
    ]

    # completion = {"size": 50}
    # pagination_class = PageNumberPagination
    # page_size = 50
    # page = 1
    pagination_class = QueryFriendlyPageNumberPagination

    search_fields = {
        "song_name": {"fuzziness": "2"},
        "album.title": {"fuzziness": "2"},
        "album.artist.name": {"fuzziness": "1"},
        "genre.name": {"fuzziness": "1"},
    }

    filter_fields = {"album": "album_name", "artist": "artist_name"}

    ordering = ("_score",)
