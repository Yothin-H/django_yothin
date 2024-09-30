from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name')


class ExtendedProfileForm(forms.ModelForm):
    prefix = 'extended' #to have specific name of variable
    class Meta:
        model = Profile
        fields = ('address','phone')
        labels={
            'address':'Address',
            'phone' : 'Tel.'
        }
        widgets = {
            'address':forms.Textarea(attrs={'rows':3})
        }
