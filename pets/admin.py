from django.contrib import admin
from .models import Pet

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display=("species",)
    list_display_links=("species",)