from django.urls import path
from . import views

urlpatterns =[
    path('', views.food,name='food'),
    path('<int:food_id>',views.foodd,name='foodd')
]