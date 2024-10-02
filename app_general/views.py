from django.http.response import HttpResponse
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from app_food.models import Food
from .models import Subscription
from .forms import SubscriptionForm, SubscriptionModelForm
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied

# Create your views here.
def home(request:HttpRequest):
    return render(request,'app_general/home.html')

def about(request:HttpRequest):
    if not request.user.is_superuser :
        raise PermissionDenied()
    return render(request,'app_general/about.html')

def subscription(request:HttpRequest):
    if request.method=='POST':
        form=SubscriptionModelForm(request.POST)
        if form.is_valid():
            # data=form.cleaned_data
            # new_sub=Subscription()
            # new_sub.name=data['name']
            # new_sub.email=data['email']
            # new_sub.save()
            # new_sub.food_set.set(data['food_set'])
            form.save()
            return HttpResponseRedirect(reverse('thankyou'))
            #return render(request,'app_general/subscription_thankyou.html')
    else:
        form = SubscriptionModelForm()
    context = {'form':form}
    return render(request,'app_general/subscription_form.html',context)

def subscription_thankyou(request:HttpRequest):
    return render(request,'app_general/subscription_thankyou.html') 

def change_theme(request:HttpRequest):
    #Referer
    referer = request.headers.get('referer')
    if referer is not None:
        response = HttpResponseRedirect(referer)
    else:
        response = HttpResponseRedirect(reverse('home'))


    #Change theme
    theme=request.GET.get('theme')
    if theme == 'dark':
        expired_date = datetime.now() + timedelta(days=365)
        response.set_cookie('theme','dark',expires=expired_date)
    else:
        response.delete_cookie('theme')
    return response