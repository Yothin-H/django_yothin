from django.shortcuts import render
from app_user.forms import RegisterForm
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
 
# add : HttpRequest because I need to get auto completion
def registerer(request: HttpRequest):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user) # register and be logged in automatically
            return HttpResponseRedirect(reverse('home'))
    else:
        form = RegisterForm()
    #GET
    context = {'form':form}
    return render(request,'app_user/register.html',context)

@login_required #to validate whether log in or not but don't forget to add LOGIN_URL in setting
def dashboard(request : HttpRequest):
    return render(request,'app_user/dashboard.html')