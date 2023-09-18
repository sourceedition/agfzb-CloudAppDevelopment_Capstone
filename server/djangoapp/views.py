from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import DealerReview
# from .restapis import related methods
from django.contrib.auth.forms import UserCreationForm
from .restapis import get_request, get_dealers_from_cf, get_dealer_reviews_from_cf, analyze_review_sentiments, get_dealer_by_id, post_request
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
    return render(request, 'djangoapp/login.html')

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
    return render(request, 'djangoapp/registration.html', {'form': form})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = 'https://plumball33-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer_url = 'https://plumball33-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'
        dealer = get_dealer_by_id(dealer_id=dealer_id)
        context["dealer"] = dealer
    
        review_url = "https://plumball33-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        reviews = get_dealer_reviews_from_cf(dealer_id=dealer_id)

        # Analyze sentiment for each review
        for review in reviews:
            sentiment = analyze_review_sentiments(review)
            review.sentiment = sentiment  # Update the sentiment attribute of the review
        
        print(reviews)
        context["reviews"] = reviews
        context["dealer_id"] = dealer_id
        
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id=None):
    if request.method == 'GET':
        context = {'dealer_id': dealer_id}
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == 'POST':
        python_server_url = f"https://plumball33-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review?dealerId={dealer_id}"
        
        review_data = {
            'dealer_id': dealer_id,
            'name': request.POST.get('name'),
            'dealership': request.POST.get('dealership'),
            'review': request.POST.get('review'),
            'purchase': request.POST.get('purchase'),
            'purchase_date': request.POST.get('purchase_date'),
            'car_make': request.POST.get('car_make'),
            'car_model': request.POST.get('car_model'),
            'car_year': request.POST.get('car_year'),
        }

        # Create a dictionary for the JSON payload
        json_payload = {
            "review": review_data
        }

        # Debugging: Print the json_payload
        print("Review Data - JSON Payload:", json_payload)

        try:
            # Call the post_request method with the payload
            response = post_request(python_server_url, json_payload=json_payload, dealerId=dealer_id)

            if response.status_code == 201:
                messages.success(request, "Review posted successfully")
                
                # Immediately retrieve reviews for the same dealer_id
                reviews = get_dealer_reviews_from_cf(dealer_id)
                
                # Log the retrieved reviews for debugging
                print("Retrieved Reviews:", reviews)
            else:
                messages.error(request, "Failed to post review")
        except requests.exceptions.RequestException as e:
            messages.error(request, "Failed to post review")

        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
