from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    car_type = models.CharField(max_length=10, choices=CAR_TYPES)
    
    year = models.DateField()  # Year of the car model
    
    # Add other fields as needed

    def __str__(self):
        return f"{self.year} {self.make.name} {self.name}"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, dealer_id, name, address, city, state, zip_code):
        self.dealer_id = dealer_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, review_id, dealer_id, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        self.review_id = review_id
        self.dealer_id = dealer_id
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
