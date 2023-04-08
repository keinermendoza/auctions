from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    category =  models.CharField(max_length=100)

    def __str__(self):
        return self.category
        
class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.URLField(max_length=264, blank=True)
    date = models.DateTimeField(default=datetime.now)
    active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="listings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offerts")
    followers = models.ManyToManyField(User, related_name="favorites", blank=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def count(self):
        return self.bid.count()

    def short_description(self):
        """return the entire description if is lees than the "limit" characters
        else return a sub-string cutted at the last word lees than "limit" characters,
        adding '...' at the end"""

        limit = 50
        if len(self.description) >= limit:
            description = self.description[:limit]
            i = description.rfind(" ")
            return f"{description[:i]}..."
        else:
            return self.description

    def short_name(self):
        """return the entire name if is lees than the "limit" characters
        else return a sub-string cutted at the last word lees than "limit" characters,
        adding '...' at the end"""

        limit = 25
        if len(self.name) >= limit:
            title = self.name[:limit]
            i = title.rfind(" ")
            return f"{title[:i]}..."
        else:
            return self.name


class Comment(models.Model):

    date = models.DateTimeField(default=datetime.now)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    listing = models.ForeignKey(Listing, related_name="comment", on_delete=models.CASCADE)

    def __str__(self):
        return f"A comment of {self.user}"


class Bid(models.Model):

    price = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    offerent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")

    def clean(self):
        """Check that bid price be almost equal to original price when there are no previous bid and greater than actual price when bids already exist"""
        
        # get the listing for know it's price
        listing = Listing.objects.get(pk=self.listing.id)
        
        # get the best bid for listing
        best_bid = Bid.objects.filter(listing=self.listing.id).order_by("-price").first()

        # When there are no previous bids
        if best_bid is None:        

            if self.price < listing.price:
                raise ValidationError(
                    {
                        "price": f"The price must be at least {listing.price}"
                    }
                )
            else:
                listing.price = self.price
                listing.without_bid = False
                listing.save()

        # When other bids already exist
        else:
            if self.price < listing.price + 1:
                raise ValidationError({"price": f"The price must be at least {listing.price + 1}"})
            else:
                listing.price = self.price
                listing.save()

    def __str__(self):
        return f"{self.offerent} offers {self.price} by {self.listing}"




#     CATEGORIES_CHOICES = (
#         ("NONE", "No Category Listed"),
#         ("TEC", "Tecnology"),
#         ("MAG", "Magic"),
#         ("FOOD", "Food"),
#         ("CLOTHE", "Clothe"),
#     )
#     @classmethod
#     def categories_dicts(cls):
#         return [{"value":categories[0],"name":categories[1]} for categories in cls.CATEGORIES_CHOICES]