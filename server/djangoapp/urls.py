from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('static/', views.static_django_view, name='static_django'),

    # path for about view
    path('about/', views.about_view, name='about'),

    # path for contact us view
    path('contact/', views.contact_view, name='contact'),

    # path for registration
    path('signup/', views.custom_signup, name='custom_signup'),

    # path for login
    path('login/', views.custom_login, name='custom_login'),

    # path for logout
    path('logout/', views.custom_logout, name='custom_logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
