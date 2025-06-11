from django.contrib import admin
from .models import Listings, Bids, Comments

# Register your models here.
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Comments)