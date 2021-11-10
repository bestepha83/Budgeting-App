from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Project, Expense, Income
from django.views.generic import CreateView
from django.utils.text import slugify
from .forms import ExpenseForm, IncomeForm
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from . forms import UserRegisterForm

def register(request):
    if request.method == "POST": 
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account was created succesfully')
            return redirect('profile')
        else: 
            form = UserRegisterForm()
    return render(request, 'budget/register.html', {'form': form})

def accounts(request):
    project_list = Project.objects.all()
    return render(request, 'budget/accounts.html', {'project_list': project_list})

def profile(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    project_list = Project.objects.all()
    return render(request, 'budget/profile.html', {'project': project, 'project_list': project_list, 'expense_list': project.expenses.all()})

def transactions(request, project_slug):
    project_list = Project.objects.all()
    project = get_object_or_404(Project, slug=project_slug)
    if request.method == "GET":
        return render(request, 'budget/transactions.html', {'project': project, 'project_list': project_list, 'expense_list': project.expenses.all(), 'income_list': project.income.all()})
    elif request.method == "POST":
        expenseform = ExpenseForm(request.POST)
        incomeform = IncomeForm(request.POST)
        if request.POST['action'] == 'expense' and expenseform.is_valid():
            title = expenseform.cleaned_data['title']
            amount = expenseform.cleaned_data['amount']
            date = expenseform.cleaned_data['date']
        
            Expense.objects.create(
                project = project,
                title = title,
                amount = amount,
                date = date,
            ).save()
        elif request.POST['action'] == 'income' and incomeform.is_valid():
            title = incomeform.cleaned_data['title']
            amount = incomeform.cleaned_data['amount']
            date = incomeform.cleaned_data['date']
        
            Income.objects.create(
                project = project,
                title = title,
                amount = amount,
                date = date,
            ).save()
    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()
        # income = get_object_or_404(Income, id=incomeid)
        # income.delete()
        return HttpResponse('')
    return render(request, 'budget/transactions.html', {'project': project, 'project_list': project_list, 'expense_list': project.expenses.all(), 'income_list': project.income.all()})

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'budget/add-project.html'
    fields = ('name', 'budget')

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['name'])