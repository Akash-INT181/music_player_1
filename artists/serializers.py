from rest_framework import serializers

# from songs.serializers import SongReadOnlySerializer

# from songs.serializers import SongSerializer
from .models import Artist, Album


class AlbumOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["id", "album_name", "created_at"]


class ArtistSerializer(serializers.ModelSerializer):
    albums = AlbumOnlySerializer(many=True, required=False)

    class Meta:
        model = Artist
        fields = "__all__"


class ArtistOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "artist_name"]


class AlbumSerializer(serializers.ModelSerializer):
    # songs = SongSerializer(many=True, required=False)
    artist = ArtistOnlySerializer(many=False)

    class Meta:
        model = Album
        fields = "__all__"


class AlbumArtistSeralizer(serializers.ModelSerializer):
    # artist_name = serializers.ReadOnlyField(source="album.artist.artist_name")
    artist = ArtistOnlySerializer(many=False)

    class Meta:
        model = Album
        fields = ["artist", "id", "album_name"]
