from django.shortcuts import render
from app_user.forms import RegisterForm

# Create your views here.
 
def registerer(request):
    form = RegisterForm()
    context = {'form':form}
    return render(request,'app_user/register.html',context)