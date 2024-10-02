from django.http.response import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import Food
from .forms import FavoriteFoodForm
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app_user.models import UserFavoriteFood
from django.urls import reverse

# Create your views here.
def food(request):
    all_food=Food.objects.order_by('-is_premium')
    context={'foods':all_food}
    return render(request,'app_food/food.html',context)

def foodd(request:HttpRequest, food_id):
    one_food=None
    is_favorited_food = False
    try:
        one_food=Food.objects.get(id=food_id)
        if request.user.is_authenticated:
            user_favorite_food = UserFavoriteFood.objects.get(
                user=request.user,
                food=one_food
            )
            is_favorited_food = user_favorite_food is not None
    except:
        print('No available menu')
    # try :
    #     one_food=[f for f in all_food if f['id']== food_id][0]
    # except IndexError:
    #     print('No available menu')
    form = FavoriteFoodForm()

    context = {
        'food':one_food,
        'form':form,
        'is_favorited_food':is_favorited_food
    }
    return render(request,'app_food/foodd.html',context)  

@login_required
def favorite_food(request:HttpRequest, food_id):
    if request.method == 'POST':
        form = FavoriteFoodForm(request.POST)
        if form.is_valid():
            #Static save
            # user_favorite_food:UserFavoriteFood = form.save(commit=False)
            # user_favorite_food.user=request.user #check which user did this
            # user_favorite_food.food=Food(id=food_id)
            # user_favorite_food.save()

            #Dynamic save
            obj , is_created = UserFavoriteFood.objects.update_or_create(
                defaults={'level':form.cleaned_data.get('level')},
                user = request.user,
                food=Food(id=food_id)
            )
            print ('Create favorite' if is_created else 'Update')

    return HttpResponseRedirect(request.headers.get('referer'))


@login_required
def unfavorite_food(request:HttpRequest, food_id):
    if request.method == 'POST':
        request.user.favorite_food_set.remove(Food(id=food_id))
    return HttpResponseRedirect(reverse('dashboardeiei'))