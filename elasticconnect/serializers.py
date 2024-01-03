from rest_framework import serializers
from artists.models import Album, Artist

# from .elastic_search_config import es

import json
from songs.models import Genre, Rating, Song


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class AlbumSerializers(serializers.ModelSerializer):
    artist = ArtistSerializer(many=False)

    class Meta:
        model = Album
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class SongSerializers(serializers.ModelSerializer):
    album = AlbumSerializers(many=False)
    genre = GenreSerializer(many=False)
    # rating = RatingSerializer(many=True)

    class Meta:
        model = Song
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(representation)
        data = {}
        # for key, val in representation.items():
        #     print(key, val)
        #     if key == "id":
        #         data[key] = val
        #     elif key == "album":
        #         data[key + "_id"] = val["id"]
        #         data[key] = val["album_name"]
        #         data["artist_id"] = val["artist"]["id"]
        #         data["artist_name"] = val["artist"]["artist_name"]
        #     elif key == "genre":
        #         data[key + "_id"] = val["id"]
        #         data[key + "_name"] = val[key + "_name"]
        #     else:
        #         data[key] = val
        # # print(data)
        # es.index(index="search-song-index", body=data, id=data["id"])

        return representation
