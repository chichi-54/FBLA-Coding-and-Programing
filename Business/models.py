from django.db import models
import uuid
from Users.models import Profile
# Create your models here.

class Business(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.ForeignKey("Status", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.ForeignKey("Address", on_delete=models.CASCADE)
    phone_number = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.name


class Status(models.Model):
    OPTIONS =(
        ("Approved", "APPROVED"),
        ("Pending", "Pending"),
        ("Declined", "Declinedz")
    )
    approval_state = models.CharField(max_length=10, choices=OPTIONS)
    def __str__(self):
        return self.approval_state
    

class Address(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    street_address = models.CharField(max_length=200)
    street_address_2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return self.street_address + " " + self.city + " " + self.state + " " + self.country + " " + self.zip_code


class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    business = models.ForeignKey("Business", on_delete=models.CASCADE)
    review_message = models.TextField(blank=True)
    review_rating = models.ForeignKey("Rating", on_delete=models.SET_NULL, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review_rating
    

class Category(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    descritpion = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Rating(models.Model):
    OPTIONS = [
        ("Excellent", 5),
        ("Very Good", 4),
        ("Moderate", 3),
        ("Not Satisfied", 2),
        ("Awful", 1)
    ]

    rating = models.CharField(max_length=20, choices=OPTIONS)
    
    def __str__(self):
        return self.rating