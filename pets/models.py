from django.db import models

class Pet(models.Model):
    
    class AnimalSpeciesChoices(models.TextChoices):
        cat="cat","cat"
        dog="dog", "dog"
        fish="fish","fish"
        hamseter="hamster","hamster"
        reptile="reptile","reptile"
        rabbit="rabbit","rabbit"
        other="other","other"
    
    species=models.CharField(
        max_length=255,
        choices=AnimalSpeciesChoices.choices,
    )
    def __str__(self) -> str:
        return self.species