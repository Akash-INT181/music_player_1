from django.http import Http404, JsonResponse
from rest_framework import serializers, status

# from songs.serializers import SongReadOnlySerializer

# from songs.serializers import SongSerializer
from .models import Artist, Album

from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.contrib.auth.hashers import make_password, check_password


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
    artist = ArtistOnlySerializer(many=False, read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source="artist", write_only=True
    )

    class Meta:
        model = Album
        fields = "__all__"


class AlbumArtistSeralizer(serializers.ModelSerializer):
    # artist_name = serializers.ReadOnlyField(source="album.artist.artist_name")
    artist = ArtistOnlySerializer(many=False)

    class Meta:
        model = Album
        fields = ["artist", "id", "album_name"]


class ArtistAuthSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        artist = Artist.objects.create(
            artist_name=validated_data["artist_name"],
            password=make_password(validated_data["password"]),
        )
        return artist

    class Meta:
        model = Artist
        fields = "__all__"


class CustomTokenObtainPairSerializerArtist(TokenObtainSerializer):
    username_field = "artist_name"

    # USER_ID_CLAIM = "artist_id"
    # USER_ID_FIELD = "id"

    def create_token(self, user):
        refresh = RefreshToken.for_user(user)

        access_token = refresh.access_token
        access_token["is_artist"] = True
        refresh["is_artist"] = True
        if "user_id" in access_token:
            del access_token["user_id"]
        if "user_id" in refresh:
            del refresh["user_id"]
        access_token["artist_id"] = int(user.id)
        refresh["artist_id"] = int(user.id)

        return {
            "refresh": str(refresh),
            "access": str(access_token),
            "artist_id": str(user.id),
            "artist_name": user.artist_name,
        }

    def validate(self, attrs):
        try:
            artist_instance = get_object_or_404(
                Artist, artist_name=attrs["artist_name"]
            )
        except Http404:
            raise serializers.ValidationError("Artist not found")

        artist_data = ArtistAuthSerializer(artist_instance).data

        if not check_password(attrs["password"], artist_data["password"]):
            raise serializers.ValidationError("Incorrect password")

        token_data = self.create_token(artist_instance)
        return token_data
