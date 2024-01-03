from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Song


@registry.register_document
class SongDocument(Document):
    id = fields.IntegerField(
        attr="id",
    )

    song_name = fields.TextField(
        attr="song_name",
        fields={
            "raw": fields.TextField(),
        },
    )

    track_no = fields.IntegerField(
        attr="track_no",
    )

    played = fields.IntegerField(
        attr="played",
    )

    genre = fields.ObjectField(
        attr="genre",
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(attr="genre_name"),
        },
    )

    album = fields.ObjectField(
        attr="album",
        properties={
            "id": fields.IntegerField(),
            "title": fields.TextField(
                attr="album_name",
                fields={
                    "raw": fields.KeywordField(),
                },
            ),
            "artist": fields.ObjectField(
                attr="artist",
                properties={
                    "id": fields.IntegerField(),
                    "name": fields.TextField(
                        attr="artist_name",
                        fields={
                            "raw": fields.KeywordField(),
                        },
                    ),
                },
            ),
        },
    )

    class Index:
        name = "search-postgres"

    class Django:
        model = Song
