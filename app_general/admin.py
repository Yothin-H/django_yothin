from django.contrib import admin
from .models import Subscription

# Register your models here.
class SubscriptionAdmin(admin.ModelAdmin):
    list_display=['name','email','status','registered']
    search_fields=['name']
    list_filter=['status']

admin.site.register(Subscription, SubscriptionAdmin)