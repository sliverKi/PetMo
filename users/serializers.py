from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError,ValidationError
from .models import User, Address
from pets.serializers import PetsSerializers
from pets.models import Pet



class TinyUserSerializers(ModelSerializer):
    #user 정보 : username, profile, pets, region,/ 작성 글(게시글, [댓글, 대댓글]이 있는 게시글)
    pets= PetsSerializers(many=True)
    regionDepth2=serializers.CharField(source="user_address.regionDepth2", read_only=True)
    regionDepth3=serializers.CharField(source="user_address.regionDepth3", read_only=True)

    class Meta:
        model=User
        fields=("username","profile","pets","regionDepth2","regionDepth3")

class AddressSerializers(serializers.ModelSerializer):
    user=TinyUserSerializers(read_only=True)
    class Meta:
        model = Address
        fields = (
            "id",
            "user",
            "addressName",
            "regionDepth1", 
            "regionDepth2",
            "regionDepth3",
        )
class PrivateUserSerializers(ModelSerializer):
    pets=PetsSerializers(many=True)
    regionDepth2=serializers.CharField(source="user_address.regionDepth2", read_only=True)
    regionDepth3=serializers.CharField(source="user_address.regionDepth3", read_only=True)
    class Meta:
        model=User
        fields=(
            "username",
            "profile",
            "pets",
            "regionDepth2",
            "regionDepth3"
            )
        
    def update(self, instance, validated_data):
        pets_data = validated_data.pop("pets", None)
        if pets_data is not None:
            if not isinstance(pets_data, list):
                raise serializers.ValidationError(
                    "Pets should be provided as a list of objects"
                )
            if len(pets_data) > 3:
                raise serializers.ValidationError(
                    "A maximum of 3 pets can be selected."
                )
            instance.pets.clear()
            for pet in pets_data:
                species = pet.get("species")
                if not species:
                    raise serializers.ValidationError(
                        "Pet species should be provided."
                    )
                try:
                    pet_obj = Pet.objects.get(species=species)
                    instance.pets.add(pet_obj)
                except Pet.DoesNotExist:
                    raise serializers.ValidationError(
                        f"{species} is not a valid pet species."
                    )
        return super().update(instance, validated_data)
    




class UserSerializers(ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

