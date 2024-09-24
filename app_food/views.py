from django.http.response import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import Food

# Create your views here.
def food(request):
    all_food=Food.objects.order_by('-is_premium')
    context={'foods':all_food}
    return render(request,'app_food/food.html',context)

def foodd(request, food_id):
    one_food=None
    try:
        one_food=Food.objects.get(id=food_id)
    except:
        print('No available menu')
    # try :
    #     one_food=[f for f in all_food if f['id']== food_id][0]
    # except IndexError:
    #     print('No available menu')

    context = {'food':one_food}
    return render(request,'app_food/foodd.html',context) 