from django.contrib import admin

from .models import Profile, Auction, Bid

# Register your models here.
admin.site.register(Profile)
admin.site.register(Auction)
admin.site.register(Bid)

