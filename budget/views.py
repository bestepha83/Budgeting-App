from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Project, Expense
from django.views.generic import CreateView
from django.utils.text import slugify
from .forms import ExpenseForm
import json

def accounts(request):
    project_list = Project.objects.all()
    return render(request, 'budget/accounts.html', {'project_list': project_list})

def profile(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    if request.method == "GET":
        form = ExpenseForm(request.GET)
        return render(request, 'budget/profile.html', {'project': project, 'expense_list': project.expenses.all(), 'form': form})
    elif request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']
        
            Expense.objects.create(
                project = project,
                title = title,
                amount = amount,
                date = date,
            ).save()
    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()
        return HttpResponse('')
    return HttpResponseRedirect(project_slug)


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