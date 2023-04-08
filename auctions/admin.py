from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.core.exceptions import ValidationError
from django import forms
from .models import User, Comment, Listing, Bid, Category
# Register your models here.

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)

# example of actions in admin taked from youtube
def active(modeladmin, request, queryset):
    for obj in queryset:
        obj.active = True
        obj.save()

# example of actions in admin taked from youtube
def desactive(modeladmin, request, queryset):
    queryset.update(active=False)


class CategoriesAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    form = MyUserCreationForm
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "message", "date")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "name", "price", "active", "best_bidder", "best_price")
    actions = [desactive, active]
    @admin.display(ordering="bid__price", description="Best Bidder")
    def best_bidder(self, Listing):
        bidder = Listing.bid.all()
        if bidder:
            best = bidder.order_by("-price").first()
            return best.offerent
        else:
            return ""

    @admin.display(ordering="bid__price", description="Best Price")
    def best_price(self, Listing):
        bidder = Listing.bid.all()
        if bidder:
            best = bidder.order_by("-price").first()
            return best.price
        else:
            return ""
        

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "offerent", "listing_name", "original_price", "price")

    @admin.display(ordering="listing__name", description="Listing")
    def listing_name(self, Bid):
        return Bid.listing.name

    @admin.display(ordering="listing__price", description="Original Price")
    def original_price(self, Bid):
        return Bid.listing.price

        
admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category)