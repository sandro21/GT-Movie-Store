
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Movie, Review, MoviePetition, PetitionVote, Favorite

def index(request):
	search_term = request.GET.get('search')
	if search_term:
		movies = Movie.objects.filter(name__icontains=search_term)
	else:
		movies = Movie.objects.all()
	
	# Get favorited movie IDs for the current user
	favorited_ids = set()
	if request.user.is_authenticated:
		favorited_ids = set(Favorite.objects.filter(user=request.user).values_list('movie_id', flat=True))
	
	template_data = {
		'title': 'Movies', 
		'movies': movies,
		'favorited_ids': favorited_ids
	}
	return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
	movie = get_object_or_404(Movie, id=id)
	reviews = Review.objects.filter(movie=movie).order_by('-date')
	is_favorited = False
	if request.user.is_authenticated:
		is_favorited = Favorite.objects.filter(movie=movie, user=request.user).exists()
	template_data = {
		'title': movie.name,
		'movie': movie,
		'reviews': reviews,
		'is_favorited': is_favorited,
	}
	return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
	if request.method == 'POST' and request.POST.get('comment', '').strip():
		movie = get_object_or_404(Movie, id=id)
		Review.objects.create(
			comment=request.POST['comment'].strip(),
			movie=movie,
			user=request.user
		)
	return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
	review = get_object_or_404(Review, id=review_id)
	# Only owner may edit
	if request.user != review.user:
		return redirect('movies.show', id=id)

	if request.method == 'GET':
		template_data = {'title': 'Edit Review', 'review': review}
		return render(request, 'movies/edit_review.html', {'template_data': template_data})

	if request.method == 'POST' and request.POST.get('comment', '').strip():
		review.comment = request.POST['comment'].strip()
		review.save()
	return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
	review = get_object_or_404(Review, id=review_id, user=request.user)
	review.delete()
	return redirect('movies.show', id=id)


# Petition Views
def petitions(request):
	petitions = MoviePetition.objects.filter(is_active=True).order_by('-created_at')
	template_data = {'title': 'Movie Petitions', 'petitions': petitions}
	return render(request, 'movies/petitions.html', {'template_data': template_data})


@login_required
def create_petition(request):
	if request.method == 'POST':
		title = request.POST.get('title', '').strip()
		description = request.POST.get('description', '').strip()
		
		if title and description:
			petition = MoviePetition.objects.create(
				title=title,
				description=description,
				created_by=request.user
			)
			messages.success(request, 'Petition created successfully!')
			return redirect('movies.petitions')
		else:
			messages.error(request, 'Please fill in all fields.')
	
	template_data = {'title': 'Create Movie Petition'}
	return render(request, 'movies/create_petition.html', {'template_data': template_data})


@login_required
def vote_petition(request, petition_id):
	if request.method == 'POST':
		petition = get_object_or_404(MoviePetition, id=petition_id, is_active=True)
		
		# Check if user already voted
		existing_vote = PetitionVote.objects.filter(petition=petition, user=request.user).first()
		
		if existing_vote:
			return JsonResponse({'success': False, 'message': 'You have already voted for this petition.'})
		
		# Create vote
		PetitionVote.objects.create(petition=petition, user=request.user)
		
		# Update vote count
		petition.vote_count += 1
		petition.save()
		
		return JsonResponse({'success': True, 'message': 'Vote recorded successfully!', 'vote_count': petition.vote_count})
	
	return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
def petition_detail(request, petition_id):
	petition = get_object_or_404(MoviePetition, id=petition_id, is_active=True)
	user_has_voted = PetitionVote.objects.filter(petition=petition, user=request.user).exists()
	
	template_data = {
		'title': petition.title,
		'petition': petition,
		'user_has_voted': user_has_voted
	}
	return render(request, 'movies/petition_detail.html', {'template_data': template_data})


# Favorite Views
@login_required
def toggle_favorite(request, id):
	movie = get_object_or_404(Movie, id=id)
	favorite, created = Favorite.objects.get_or_create(movie=movie, user=request.user)
	
	if not created:
		# Already favorited, so remove it
		favorite.delete()
		messages.success(request, f'{movie.name} removed from favorites.')
		return redirect('movies.show', id=id)
	else:
		# Newly favorited
		messages.success(request, f'{movie.name} added to favorites!')
		return redirect('movies.show', id=id)


@login_required
def favorites(request):
	favorites_list = Favorite.objects.filter(user=request.user).order_by('-created_at')
	movies = [fav.movie for fav in favorites_list]
	template_data = {'title': 'My Favorites', 'movies': movies}
	return render(request, 'movies/favorites.html', {'template_data': template_data})

# Create your views here.
