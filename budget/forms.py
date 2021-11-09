from django import forms

class ExpenseForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    date = forms.DateField()
    category = forms.ChoiceField()

class IncomeForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    date = forms.DateField()
    category = forms.ChoiceField()