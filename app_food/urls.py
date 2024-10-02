from django.urls import path
from . import views

urlpatterns =[
    path('', views.food,name='food'),
    path('<int:food_id>',views.foodd,name='foodd'),
    path('<int:food_id>/favorite', views.favorite_food,name='favfood'),
    path('<int:food_id>/unfavorite', views.unfavorite_food,name='unfavfood'),
]