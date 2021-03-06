from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Project, Expense, Income
from django.views.generic import CreateView
from django.utils.text import slugify
from .forms import ExpenseForm, IncomeForm, TickerForm, UserRegisterForm
from .tiingo import get_meta_data, get_price_data
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def home(request):
    project_list = Project.objects.all()

    return render(request, 'budget/home.html', {
        'project_list': project_list, 
    })

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'budget/register.html', {'form': form})

@login_required()
def accounts(request):
    project_list = Project.objects.all()
    return render(request, 'budget/accounts.html', {'project_list': project_list})

@login_required()
def profile(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    project_list = Project.objects.all()

    return render(request, 'budget/profile.html', {
        'project': project,
        'project_list': project_list, 
        'expense_list': project.expenses.all(),
    })

@login_required()
def transactions(request, project_slug):
    project_list = Project.objects.all()
    project = get_object_or_404(Project, slug=project_slug)
    if request.method == "GET":
        return render(request, 'budget/transactions.html', {
            'project': project, 'project_list': project_list, 
            'expense_list': project.expenses.all(), 
            'income_list': project.income.all()})
    elif request.method == "POST":
        expenseform = ExpenseForm(request.POST)
        incomeform = IncomeForm(request.POST)
        if request.POST['action'] == 'expense' and expenseform.is_valid():
            title = expenseform.cleaned_data['title']
            amount = expenseform.cleaned_data['amount']
            date = expenseform.cleaned_data['date']
            category = expenseform.cleaned_data['category']
        
            Expense.objects.create(
                project = project,
                title = title,
                amount = amount,
                date = date,
                category = category,
            ).save()
        elif request.POST['action'] == 'income' and incomeform.is_valid():
            title = incomeform.cleaned_data['title']
            amount = incomeform.cleaned_data['amount']
            date = incomeform.cleaned_data['date']
            category = incomeform.cleaned_data['category']

            Income.objects.create(
                project = project,
                title = title,
                amount = amount,
                date = date,
                category = category,
            ).save()
    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        try:
            expense = get_object_or_404(Expense, id=id)
            expense.delete()
        except:
            income = get_object_or_404(Income, id=id)
            income.delete()
    return render(request, 'budget/transactions.html', {
        'project': project, 
        'project_list': project_list, 
        'expense_list': project.expenses.all(), 
        'income_list': project.income.all()
        })


@login_required()
def analytics(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    project_list = Project.objects.all()
    return render(request, 'budget/analytics.html', {
        'project': project,
        'project_list': project_list, 
    })

def total_spent_info(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    expenses = project.expenses.all()
    income = project.income.all()
    finalrep = {}

    def get_initial_budget(project):
        return project.budget

    def get_expenses(expense):
        amount = 0
        for expense in expenses:
            amount += expense.amount
        return amount
    
    def get_income(income):
        amount = 0
        for check in income:
            amount += check.amount
        return amount
    
    def get_current_budget(project):
        return project.budget - get_expenses(expenses) + get_income(income)

    finalrep["Initial"] = get_initial_budget(project)
    finalrep["Current"] = get_current_budget(project)
    finalrep["Expenses"] = get_expenses(expenses)
    finalrep["Income"] = get_income(income)
    return JsonResponse({'total_spent_info': finalrep}, safe=False)

def expense_category_info(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    expenses = project.expenses.all()
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_info': finalrep}, safe=False)


def expense_time_info(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    expenses = project.expenses.all()
    finalrep = {}

    def get_date(expense):
        return str(expense.date)
    date_list = list(set(map(get_date, expenses)))
    date_list.sort()
    
    def get_expense_date_amount(date):
        amount = 0
        filtered_by_date = expenses.filter(date=date)

        for item in filtered_by_date:
            amount += item.amount
        return amount

    for x in expenses:
        for y in date_list:
            finalrep[y] = get_expense_date_amount(y)

    return JsonResponse({'expense_time_info': finalrep}, safe=False)

def income_time_info(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    incomes = project.income.all()
    finalrep = {}

    def get_date(income):
        return str(income.date)
    date_list = list(set(map(get_date, incomes)))
    date_list.sort()
    
    def get_income_date_amount(date):
        amount = 0
        filtered_by_date = incomes.filter(date=date)

        for item in filtered_by_date:
            amount += item.amount
        return amount

    for x in incomes:
        for y in date_list:
            finalrep[y] = get_income_date_amount(y)

    return JsonResponse({'income_time_info': finalrep}, safe=False)

@login_required()  
def stocks(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    project_list = Project.objects.all()    
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect(f'stocks/{ticker}')
    else:
        form = TickerForm()
    
    return render(request, 'budget/stocks.html', {
        'form': form,
        'project': project,
        'project_list': project_list,
        })

@login_required()
def ticker(request, tid, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    project_list = Project.objects.all()    
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect(f'{ticker}')
    else:
        form = TickerForm()
    context = {}
    context['ticker'] = tid
    context['meta'] = get_meta_data(tid)
    context['price'] = get_price_data(tid)
    context['form'] = form
    context['project'] = project
    context['project_list'] = project_list
    return render(request, 'budget/ticker.html', context)



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