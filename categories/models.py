from django.db import models


class Category(models.Model):
    class PostKindChoices(models.TextChoices):
        Free="Free","Free"
        Question="Question", "Question"
        Master="Master","Master"
        Review="Review","Review"
        Congrats="Congrats","Congrats"
        Help="Help","Help"
    type = models.CharField(
        max_length=255,
        choices=PostKindChoices.choices,
    )
    def __str__(self) -> str:
        return self.type

    
