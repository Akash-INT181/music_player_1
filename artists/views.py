from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from songs.serializers import (
    AlbumReadOnlySerializer,
    SongCreateSerializer,
    SongSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User

from .serializers import (
    AlbumSerializer,
    ArtistAuthSerializer,
    ArtistSerializer,
    CustomTokenObtainPairSerializerArtist,
)

from songs.models import Genre, Song
from .models import Artist, Album
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView

import pandas as pd

from django.contrib.auth import get_user_model


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        artist_id = validated_token.get("artist_id")
        if artist_id:
            try:
                return Artist.objects.get(id=artist_id)
            except Artist.DoesNotExist:
                return None
        else:
            user_id = validated_token.get("user_id")
            if user_id:
                User = get_user_model()
                try:
                    return User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return None
        return None


class HasAnyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # Define the required permissions for the view
        # required_permissions = ["permission1", "permission2", "permission3"]
        # Allow GET requests for all users
        # print(isinstance(request.user, Artist))
        if request.method == "GET" and (
            isinstance(request.user, Artist) or isinstance(request.user, User)
        ):
            return True
        if isinstance(request.user, Artist) and request.method in [
            "POST",
            "PUT",
            "PATCH",
        ]:
            return True

        return False
        # Check if the user has any of the specified permissions


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasAnyPermissions]


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasAnyPermissions]


class AlbumSongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasAnyPermissions]

    def get_queryset(self):
        album_id = self.kwargs.get("album_id")
        return Song.objects.filter(album_id=album_id).order_by("track_no")

    @action(detail=False, methods=["post"], url_path="create_songs")
    def create_songs(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = SongCreateSerializer(data=request.data, many=True)
        else:
            serializer = SongCreateSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(album_id=self.kwargs.get("album_id"))


class ArtistSongViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlbumReadOnlySerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [HasAnyPermissions]

    def get_queryset(self):
        artist_id = self.kwargs.get("artist_id")
        return Album.objects.filter(artist_id=artist_id).order_by("created_at")


@api_view(["GET"])
def create_album(request):
    df = pd.read_csv("D:\\DRF\\music_player_1\\rare.csv", header=0)
    aid = Album.objects.create(
        album_name=df.loc[0]["album"],
        artist=Artist.objects.get(artist_name="Selena Gomez"),
    )
    aid.save()
    for index, row in df.iterrows():
        print(index, row.to_dict())
        row = row.to_dict()
        gid = Genre.objects.get(genre_name=row["genre"])
        song = Song.objects.create(
            song_name=row["song_name"],
            track_no=row["track_no"],
            album=aid,
            genre=gid,
            song_file="https://drive.google.com/file/d/1X2S--ALE7IEY4SrRudsQ5pOVPxVm2yrG/view?usp=drive_link",
        )
        song.save()
    return Response("ok")


class ArtistRegisterViewSet(APIView):
    serializer_class = ArtistAuthSerializer

    def post(self, request):
        serializer = ArtistAuthSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            user = Artist.objects.create(
                artist_name=data["artist_name"],
                password=make_password(data["password"]),
            )
            user.save()
            return Response({"artist_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializerArtist
