from django.contrib.auth.decorators import login_required
from .models import Order, Item
@login_required
def purchase(request):
	cart = request.session.get('cart', {})
	movie_ids = list(cart.keys())
	if movie_ids == []:
		return redirect('cart.index')

	movies_in_cart = Movie.objects.filter(id__in=movie_ids)
	cart_total = calculate_cart_total(cart, movies_in_cart)

	# Create order
	order = Order(user=request.user, total=cart_total)
	order.save()

	# Create items
	for movie in movies_in_cart:
		qty = int(cart[str(movie.id)])
		Item.objects.create(
			order=order,
			movie=movie,
			price=movie.price,
			quantity=qty
		)

	# Clear cart
	request.session['cart'] = {}

	template_data = {
		'title': 'Purchase confirmation',
		'order_id': order.id
	}
	return render(request, 'cart/purchase.html', {'template_data': template_data})
from django.shortcuts import render, redirect, get_object_or_404
from movies.models import Movie
from .utils import calculate_cart_total

def index(request):
	cart = request.session.get('cart', {})
	movie_ids = [int(k) for k in cart.keys()]
	movies_in_cart = Movie.objects.filter(id__in=movie_ids) if movie_ids else []
	cart_total = calculate_cart_total(cart, movies_in_cart) if movies_in_cart else 0

	template_data = {
		'title': 'Cart',
		'movies_in_cart': movies_in_cart,
		'cart_total': cart_total,
	}
	return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
	# ensure movie exists
	get_object_or_404(Movie, id=id)

	# read current cart (ids as STRING keys)
	cart = request.session.get('cart', {})

	# quantity from form
	qty = int(request.POST.get('quantity', 1))

	# OPTION A: overwrite quantity (matches book)
	# cart[id] won't persist well as int key -> use str
	cart[str(id)] = str(qty)

	# OPTION B (nicer UX): accumulate quantity
	# cart[str(id)] = str(int(cart.get(str(id), 0)) + qty)

	request.session['cart'] = cart
	return redirect('cart.index')

def clear(request):
	request.session['cart'] = {}
	return redirect('cart.index')
from django.shortcuts import render

# Create your views here.
