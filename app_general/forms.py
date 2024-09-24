from django import forms
from app_food.models import Food
from .models import Subscription


class FoodMultipleChoiceFeild(forms.ModelMultipleChoiceField):
    def label_from_instance(self,obj):
        return obj.title
        



class SubscriptionForm(forms.Form):
    name =forms.CharField(max_length=60, required=True, label='Name-Lastname')
    email =forms.EmailField(max_length=60, required=True, label='Email')
    food_set =FoodMultipleChoiceFeild(
        queryset=Food.objects.order_by('-is_premium'),
        required=True,
        label='Interested menu',
        widget=forms.CheckboxSelectMultiple()
    )
    accepted=forms.BooleanField(required=True, label='Eiei Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veritatis, debitis?')


class SubscriptionModelForm(forms.ModelForm):
    food_set =FoodMultipleChoiceFeild(
        queryset=Food.objects.order_by('-is_premium'),
        required=True,
        label='Interested menu',
        widget=forms.CheckboxSelectMultiple()
    )
    accepted=forms.BooleanField(required=True, label='Eiei Lorem ipsum dolor sit amet, consectetur adipisicing elit. Veritatis, debitis?')
    class Meta:
        model = Subscription
        fields = ['name','email','food_set','accepted']
        labels={
            'name':'Name-Lastname',
            'email':'E-mail',
            'food_set':'Interested menu'
        }