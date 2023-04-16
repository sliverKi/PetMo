from django.db import models

class Pet(models.Model):
    
    class AnimalSpeciesChoices(models.TextChoices):
        Cat="Cat","Cat"
        DOG="Dog", "Dog"
        Fish="Fish","Fish"
        Hamseter="Hamster","Hamster"
        Reptile="Reptile","Reptile"
        Rabbit="Rabbit","Rabbit"
        Other="Other","Other"
    
    species=models.CharField(
        max_length=255,
        choices=AnimalSpeciesChoices.choices,
    )
    def __str__(self) -> str:
        return self.species