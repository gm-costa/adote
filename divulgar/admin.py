from django.contrib import admin
from .models import *


class AdminPet(admin.ModelAdmin):
    model = Pet
    list_display = ('nome', 'raca', 'status', 'usuario')

admin.site.register(Raca)
admin.site.register(Tag)
admin.site.register(Pet, AdminPet)
