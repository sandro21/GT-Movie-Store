from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def orders(request):
	template_data = {
		'title': 'Orders',
		'orders': request.user.order_set.all()
	}
	return render(request, 'accounts/orders.html', {'template_data': template_data})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, CustomErrorList

def signup(request):
	template_data = {'title': 'Sign Up'}
	if request.method == 'GET':
		template_data['form'] = CustomUserCreationForm()
		return render(request, 'accounts/signup.html', {'template_data': template_data})
	elif request.method == 'POST':
		form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
		if form.is_valid():
			form.save()
			return redirect('accounts.login')   # go to Login after signup
		template_data['form'] = form
		return render(request, 'accounts/signup.html', {'template_data': template_data})

def login(request):
	template_data = {'title': 'Login'}
	if request.method == 'GET':
		return render(request, 'accounts/login.html', {'template_data': template_data})
	elif request.method == 'POST':
		user = authenticate(
			request,
			username=request.POST.get('username', ''),
			password=request.POST.get('password', '')
		)
		if user is None:
			template_data['error'] = 'The username or password is incorrect.'
			return render(request, 'accounts/login.html', {'template_data': template_data})
		auth_login(request, user)
		return redirect('home.index')

@login_required
def logout(request):
	auth_logout(request)
	return redirect('home.index')
from django.shortcuts import render

# Create your views here.
