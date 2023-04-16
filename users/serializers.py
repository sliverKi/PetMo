from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import User
from pets.serializers import PetsSerializers


class TinyUserSerializers(serializers.ModelSerializer):
    #username, profile, region2 
    # pets= PetsSerializers(many=True)
    class Meta:
        model=User
        fields=("username","profile",)

