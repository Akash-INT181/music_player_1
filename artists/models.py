from django.db import models

# Create your models here.


class Artist(models.Model):
    artist_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.artist_name)


class Album(models.Model):
    album_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")

    def __str__(self):
        return str(self.album_name)
