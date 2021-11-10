from django import forms
import django
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django import forms 

class ExpenseForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    date = forms.DateField()

class IncomeForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    date = forms.DateField()
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta: 
        model = User 
        fields = ['username', 'email', 'password1', 'password2']