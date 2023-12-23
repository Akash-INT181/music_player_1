from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from elasticconnect.serializers import SongSerializers

from songs.models import Song


class ElasticViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializers
