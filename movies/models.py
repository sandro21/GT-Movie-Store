

from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	price = models.IntegerField()
	description = models.TextField()
	image = models.ImageField(upload_to='movie_images/')

	def __str__(self):
		return str(self.id) + ' - ' + self.name


class Review(models.Model):
	id = models.AutoField(primary_key=True)
	comment = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add=True)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.id} - {self.movie.name}"


class MoviePetition(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255)
	description = models.TextField()
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	vote_count = models.IntegerField(default=0)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.id} - {self.title}"


class PetitionVote(models.Model):
	id = models.AutoField(primary_key=True)
	petition = models.ForeignKey(MoviePetition, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	voted_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('petition', 'user')

	def __str__(self):
		return f"{self.user.username} voted for {self.petition.title}"

# Create your models here.
