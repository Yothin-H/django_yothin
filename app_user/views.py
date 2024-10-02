from django.shortcuts import render
from app_user.forms import RegisterForm
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, ExtendedProfileForm
from .models import CustomUser
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .utils.activation_token_generator import activation_token_generator
from .models import UserFavoriteFood

# Create your views here.
 
# add : HttpRequest because I need to get auto completion
def registerer(request: HttpRequest):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            #Register user
            user: CustomUser =form.save(commit=False)
            user.is_active=False
            user.save()

            # register and be logged in automatically
            # login(request, user) 
            
            #Build email body html
            context = {
                'protocol': request.scheme,
                'host' : request.get_host(),
                'uidb64' : urlsafe_base64_encode(force_bytes(user.id)),
                'token' : activation_token_generator.make_token(user)
            }
            email_body = render_to_string('app_user/activate_email.html',context)

            #Send E-mail
            email=EmailMessage(
                to=[user.email],
                subject='Activate account',
                body=email_body
            )
            email.send()

            return HttpResponseRedirect(reverse('registthank'))
    else:
        form = RegisterForm()
    #GET
    context = {'form':form}
    return render(request,'app_user/register.html',context)



def register_thankyou(request:HttpRequest):
    return render(request, 'app_user/register_thankyou.html')


def activate(request : HttpRequest,uidb64:str, token:str):
    title = 'Your email has activated'
    description = 'You can go log in now'
    button ='Go to log in'
    link='login'
    #Decode user id
    id = urlsafe_base64_decode(uidb64).decode()

    try :
        user: CustomUser = CustomUser.objects.get(id=id)
        if not activation_token_generator.check_token(user,token):
            raise Exception('Check token false')
        user.is_active=True
        user.save()
    except :
        print ('Failed activation')
        #In case of the link has been used
        title = 'Activation is fail'
        description = 'The link might be used'
        button ='Go to Sign up'
        link='registerrr'

    context = { 'title':title, 'description':description,'button':button,'link':link}
    return render(request,'app_user/activate.html',context)


@login_required #to validate whether log in or not but don't forget to add LOGIN_URL in setting
def dashboard(request : HttpRequest):
    favorite_food_pivots = request.user.favorite_food_pivot_set.order_by('-level')
    context = {'favorite_food_pivots':favorite_food_pivots}
    return render(request,'app_user/dashboard.html', context)


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
            response= HttpResponseRedirect(reverse('profileee'))
            response.set_cookie('is_saved','1')
            return response
    else :
        form = UserProfileForm(instance=user)
        try :
            extended_form = ExtendedProfileForm(instance=user.profile)
        except :
            extended_form = ExtendedProfileForm()
    #GET
    is_saved = request.COOKIES.get('is_saved') == '1'
    flash_message = 'Saved' if is_saved else None
    context = {
        'form':form,
        'extended_form':extended_form,
        'flash_message' : flash_message
    }
    response = render(request, 'app_user/profile.html',context)
    if is_saved:
        response.delete_cookie('is_saved')
    return response