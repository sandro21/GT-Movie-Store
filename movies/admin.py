
from django.contrib import admin
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
	ordering = ['name']             # order alphabetically
	search_fields = ['name']        # enable search by name

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)

# Register your models here.
