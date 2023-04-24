from rest_framework.serializers import ModelSerializer
from rest_framework import status
from rest_framework.exceptions import ParseError, ValidationError
from .models import Pet

class PetsSerializers(ModelSerializer):
    class Meta:
        model=Pet
        fields=("species",)
        read_only=False

    # def validate_species(self, species):
    #     if not isinstance(species, str):
    #         raise ValidationError('유효한 동물 종류가 아닙니다.')
    #     if len(species)>3:
    #         raise ValidationError("동물은 최대 3종까지만 선택이 가능합니다!")
    #     return species
    