from django.db import models
import uuid
from Users.models import Profile
# Create your models here.

class Business(models.Model):
    OPTIONS = (
        ("Approved", "Approved"),
        ("Pending", "Pending"),
        ("Declined", "Declinedz")
    )
    approval_state = models.CharField(max_length=10, choices=OPTIONS, null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    categories = models.ManyToManyField("Category", blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.ForeignKey("Address", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, default="default.jpg")
    phone_number = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    website = models.CharField(max_length=200, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ['-vote_ratio', '-vote_total', 'name']

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio



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
    OPTIONS = [
        ("Excellent", 5),
        ("Very Good", 4),
        ("Moderate", 3),
        ("Not Satisfied", 2),
        ("Awful", 1)
    ]
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    business = models.ForeignKey("Business", on_delete=models.CASCADE)
    review_message = models.TextField(blank=True)
    review_rating = models.CharField(max_length=20, choices=OPTIONS, null=True, blank=True)
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
    