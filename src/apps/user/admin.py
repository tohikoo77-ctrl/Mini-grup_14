from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Seller)
admin.site.register(SellerWallet)
admin.site.register(Client)
admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Tag)
admin.site.register(LeadStatus)
