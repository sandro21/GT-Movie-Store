from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	CONTENT_RATING_CHOICES = [
		('G', 'G'),
		('PG', 'PG'),
		('PG-13', 'PG-13'),
		('R', 'R'),
	]
	
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
	max_content_rating = models.CharField(max_length=10, choices=CONTENT_RATING_CHOICES, default='R', blank=True, null=True)

	def __str__(self):
		return f"{self.user.username}'s Profile"
