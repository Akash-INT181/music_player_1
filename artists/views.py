from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from songs.serializers import AlbumReadOnlySerializer, SongSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import AlbumSerializer, ArtistSerializer

from songs.models import Genre, Song
from .models import Artist, Album

import pandas as pd


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class AlbumSongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        album_id = self.kwargs.get("album_id")
        return Song.objects.filter(album_id=album_id).order_by("track_no")


class ArtistSongViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlbumReadOnlySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        artist_id = self.kwargs.get("artist_id")
        return Album.objects.filter(artist_id=artist_id).order_by("created_at")


@api_view(["GET"])
def create_album(request):
    df = pd.read_csv("D:\\DRF\\music_player\\harry's house.csv", header=0)
    aid = Album.objects.create(
        album_name=df.loc[0]["album"],
        artist=Artist.objects.get(artist_name=df.loc[0]["artist"]),
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
