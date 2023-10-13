from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models





class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField('Name', max_length=64)

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing_user')
    title = models.CharField('Title', max_length=256)
    description = models.TextField('Description')
    image = models.URLField('Image')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')
    status = models.BooleanField('Status', default=True)
    # watchlist = models.ManyToManyField(User, related_name='watchlist_listings', blank=True)
    created_at = models.DateTimeField('Created At', default=timezone.now, editable=False)
    
    def __str__(self):
        return f'{self.title} ({self.category})'

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Created At', default=timezone.now, editable=False)

    def __str__(self):
        return f'{self.listing} -> {self.price} -> {self.user}'

class Comment(models.Model):
    comment = models.TextField('Comment')
    user    =   models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField('Created At', default=timezone.now, editable=False)

    def __str__(self):
        return f'{self.comment} -> {self.user} -> {self.listing}'
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing')

    def __str__(self):
        return f'{self.user} -> {self.listing}'