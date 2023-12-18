from django.db import models
from artists.models import Album

from users.models import User

# Create your models here.


class Genre(models.Model):
    genre_name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return str(self.genre_name)


class Song(models.Model):
    song_name = models.CharField(max_length=40)
    track_no = models.IntegerField()
    played = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")
    song_file = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING, related_name="songs")

    def __str__(self):
        return str(self.song_name)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="rating")
    rating_number = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "song")

    def __str__(self):
        return str(self.rating_number)


class Playlist(models.Model):
    playlist_name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="playlists")
    created_at = models.DateTimeField(auto_now_add=True)
    songs = models.ManyToManyField(Song, related_name="playlists")

    def __str__(self):
        return str(self.playlist_name)
