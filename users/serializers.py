from rest_framework import serializers
from rest_framework.exceptions import ParseError
from .models import User
from pets.serializers import PetsSerializers




class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

class TinyUserSerializers(serializers.ModelSerializer):
    #username, profile, region2 
    # pets= PetsSerializers(many=True)
    class Meta:
        model=User
        fields=("username","profile",)

