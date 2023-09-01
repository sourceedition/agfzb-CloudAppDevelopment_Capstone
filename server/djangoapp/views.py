from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def static_django_view(request):
    return render(request, 'static_django.html')

# Create an `about` view to render a static about page
# def about(request):
# ...
def about_view(request):
    return render(request, 'about.html')


# Create a `contact` view to return a static contact page
#def contact(request):
def contact_view(request):
    return render(request, 'contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Logged In Successfully.')
            return redirect('djangoapp:index')
        else:
            messages.error(request, 'Please Log In.')
    return render(request, 'login.html')

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def custom_logout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully.')
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def custom_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            return redirect('djangoapp:index')  # Redirect to your desired page after registration
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://plumball33-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_from_cf(url)
        dealer_names = [dealer.short_name for dealer in dealerships]

        # Pass the 'dealer_names' variable in the context to the template
        context = {'dealer_names': dealer_names}

        return render(request, 'index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_reviews(request, dealer_id=None):
    if dealer_id is None:
        return JsonResponse({"error": "Missing 'dealer_id' parameter in the URL"}, status=400)

    python_server_url = f"http://localhost:5000/api/get_reviews?id={dealer_id}"
    try:
        response = requests.get(python_server_url)
        reviews = response.json()
        context = {'reviews': reviews}
        return render(request, 'djangoapp/dealer_details.html', context)
    except requests.exceptions.RequestException as e:
        messages.error(request, "Failed to fetch reviews")
        return render(request, 'djangoapp/dealer_details.html')

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id=None):
    if request.method == 'GET':
        context = {'dealer_id': dealer_id}
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == 'POST':
        python_server_url = "http://localhost:5000/api/post_review"
        review_data = request.POST.dict()

        try:
            response = requests.post(python_server_url, json=review_data)
            messages.success(request, "Review posted successfully")
        except requests.exceptions.RequestException as e:
            messages.error(request, "Failed to post review")

        return redirect('djangoapp:get_reviews_detail', dealer_id=dealer_id)
