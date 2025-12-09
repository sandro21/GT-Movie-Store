
from django.contrib import admin
from .models import Movie, Review, MoviePetition, PetitionVote, Favorite

class MovieAdmin(admin.ModelAdmin):
	ordering = ['name']             # order alphabetically
	search_fields = ['name']        # enable search by name

class MoviePetitionAdmin(admin.ModelAdmin):
	list_display = ['title', 'created_by', 'vote_count', 'created_at', 'is_active']
	list_filter = ['is_active', 'created_at']
	search_fields = ['title', 'description']
	ordering = ['-created_at']

class PetitionVoteAdmin(admin.ModelAdmin):
	list_display = ['user', 'petition', 'voted_at']
	list_filter = ['voted_at']
	search_fields = ['user__username', 'petition__title']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MoviePetition, MoviePetitionAdmin)
admin.site.register(PetitionVote, PetitionVoteAdmin)
admin.site.register(Favorite)

# Register your models here.
