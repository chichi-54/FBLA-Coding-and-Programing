from django.db import models
import uuid
from Users.models import Profile
# Create your models here.

import uuid
from django.db import models


class Business(models.Model):
    OPTIONS = (
        ("Approved", "Approved"),
        ("Pending", "Pending"),
        ("Declined", "Declinedz")
    )
    approval_state = models.CharField(max_length=10, choices=OPTIONS, null=True, blank=True, default="Pending")
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
        upVotes = reviews.filter(review_rating='up').count()
        downVotes = reviews.filter(review_rating='down').count()
        totalVotes = reviews.count()

        if totalVotes == 0:
            # No votes yet: assume 0% positive
            ratio = 0
            self.vote_total = 0
            self.vote_ratio = ratio
        else:
            # Percentage of positive votes
            ratio = int((upVotes / totalVotes) * 100)  # always 0-100%
            self.vote_total = totalVotes
            self.vote_ratio = ratio

        self.save()


class BusinessImage(models.Model):
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="business_images/")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.business.name}"


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
    
    @property
    def full_address(self):
        parts = [self.street_address]
        if self.street_address_2:
            parts.append(self.street_address_2)
        parts.extend([self.city, self.state, self.country, self.zip_code])
        return " ".join(parts)


class Review(models.Model):
    OPTIONS = [
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    ]
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    business = models.ForeignKey("Business", on_delete=models.SET_NULL, null=True, blank=True)
    review_message = models.TextField(blank=True)
    review_rating = models.CharField(max_length=20, choices=OPTIONS, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = [['owner', 'business']]

    def __str__(self):
        return self.review_message
    

class Category(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    descritpion = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('business_application', 'Business Application'),
        ('review_added', 'Review Added'),
        ('business_approved', 'Business Approved'),
        ('business_declined', 'Business Declined'),
    )
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.recipient.first_name} {self.recipient.last_name} - {self.message}"