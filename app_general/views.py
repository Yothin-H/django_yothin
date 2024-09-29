from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from app_food.models import Food
from .models import Subscription
from .forms import SubscriptionForm, SubscriptionModelForm

# Create your views here.
def home(request):
    return render(request,'app_general/home.html')

def about(request):
    return render(request,'app_general/about.html')

def subscription(request):
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

def subscription_thankyou(request):
    return render(request,'app_general/subscription_thankyou.html') 