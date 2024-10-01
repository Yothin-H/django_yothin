from django.urls import path, include
from . import views

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('register',views.registerer, name='registerrr'),
    path('dashboard',views.dashboard, name='dashboardeiei'),
    path('profile',views.profile, name='profileee'),
    path('register/thankyou',views.register_thankyou, name='registthank'),
    path('activate/<str:uidb64>/<str:token>',views.activate, name='activate'),
]