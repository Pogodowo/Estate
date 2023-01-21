from rest_framework import serializers
from ..models import baza_ogloszen

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=baza_ogloszen
        fields = ['tytul','cena', 'powierzchnia','lokalizacja']

