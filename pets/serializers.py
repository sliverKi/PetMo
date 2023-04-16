from rest_framework.serializers import ModelSerializer
from rest_framework import status
from rest_framework.exceptions import ParseError
from .models import Pet

class PetsSerializers(ModelSerializer):
    class Meta:
        model=Pet
        fields=("species",)

    def validate_species(self, species):
        if len(species)>3:
            raise ParseError("동물은 최대 3종까지만 선택이 가능합니다!")
        return species
    