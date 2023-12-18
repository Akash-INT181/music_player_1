from rest_framework import serializers
from artists.models import Album

from artists.serializers import AlbumArtistSeralizer
from users.serializers import UserIdSerializer, UserMinimalSerializer

# from artists.serializers import AlbumSerializer
from .models import Genre, Rating, Song, Playlist


class SongReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = (
            "id",
            "song_name",
            "track_no",
            "played",
            "created_at",
        )


class AlbumReadOnlySerializer(serializers.ModelSerializer):
    songs = SongReadOnlySerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ("id", "album_name", "songs")


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class PlaylistOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["id", "playlist_name"]


class SongSerializer(serializers.ModelSerializer):
    album = AlbumArtistSeralizer(many=False)
    genre = GenreSerializer(many=False)
    rating = RatingSerializer(many=True)
    playlists = PlaylistOnlySerializer(many=True)

    class Meta:
        model = Song
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context["request"].user
        if user.is_authenticated:
            user_id = user.id
            # print(user_id)
            playlists = instance.playlists.filter(user=user)
            representation["playlists"] = PlaylistOnlySerializer(
                playlists, many=True
            ).data
            representation["rating"] = RatingSerializer(
                instance.rating.filter(user_id=user_id), many=True
            ).data
        else:
            representation["rating"] = []
            representation["playlists"] = []

        return representation


class AddSongToPlaylistSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_internal_value(self, data):
        if isinstance(data, int):
            return {"id": data}
        return super().to_internal_value(data)


class PlaylistPostSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Playlist
        fields = "__all__"


class AllDisplayPlaylist(serializers.ModelSerializer):
    # songs = SongSerializer(many=True)
    user = UserMinimalSerializer(many=False)

    class Meta:
        model = Playlist
        fields = "__all__"


class PlaylistSongSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)
    user = UserMinimalSerializer(many=False)

    class Meta:
        model = Playlist
        fields = "__all__"


class PlaylistSerializer(serializers.ModelSerializer):
    songs = AddSongToPlaylistSerializer(many=True, required=False)

    class Meta:
        model = Playlist
        fields = ["id", "songs", "user"]

    def update(self, instance, validated_data):
        songs_data = validated_data.pop("songs", None)
        instance = super().update(instance, validated_data)

        # If there are songs to add, update the playlist's songs
        if songs_data is not None:
            if self.context["request"].method == "PATCH":
                if all(isinstance(song, int) for song in songs_data):
                    # If songs_data is a list of integers, update the playlist's songs directly
                    instance.songs.add(*songs_data)
                else:
                    # If songs_data is a list of dictionaries, extract IDs and update the playlist's songs
                    song_ids = [song.get("id") for song in songs_data]
                    instance.songs.add(*song_ids)
            elif self.context["request"].method == "PUT":
                # If PUT, remove the songs from the playlist
                if all(isinstance(song, int) for song in songs_data):
                    instance.songs.remove(*songs_data)
                else:
                    song_ids = [song.get("id") for song in songs_data]
                    instance.songs.remove(*song_ids)

        return instance
