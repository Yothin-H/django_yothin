from django.shortcuts import render
from app_user.forms import RegisterForm
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, ExtendedProfileForm

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

@login_required
def profile(request:HttpRequest):
    user = request.user
    is_new_profile = False
    #POST
    if request.method=='POST':
        form = UserProfileForm(request.POST, instance=user) #instance=request.user for update data if you don't add this, it will add another user
        try :
            #Update
            extended_form=ExtendedProfileForm(request.POST, instance=user.profile) # form with condition because this model needs to create new profile. The thing we need is if we have profile, it could edit but if not it could create
        except :
            #Create
            extended_form=ExtendedProfileForm(request.POST) #for create new profile
            is_new_profile=True

        if form.is_valid() and extended_form.is_valid():
            form.save()
            if is_new_profile:
                #Create
                profile=extended_form.save(commit=False)
                profile.user = user
                profile.save()
            else :
                #Update
                extended_form.save()
            return HttpResponseRedirect(reverse('profileee'))
    else :
        form = UserProfileForm(instance=user)
        try :
            extended_form = ExtendedProfileForm(instance=user.profile)
        except :
            extended_form = ExtendedProfileForm()
    #GET
    context = {
        'form':form,
        'extended_form':extended_form
    }
    return render(request, 'app_user/profile.html',context)