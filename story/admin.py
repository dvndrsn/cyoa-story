from django.contrib import admin

from .models import Passage, Choice, Character

# Register your models here.
admin.site.register(Passage)
admin.site.register(Choice)
admin.site.register(Character)