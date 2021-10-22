from django.db import models
from django.utils.text import slugify
import datetime

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def budget_left(self):
        expense_list = Expense.objects.filter(project=self)
        income_list = Income.objects.filter(project=self)
        total_expense_amount = 0
        total_income_amount = 0
        for expense in expense_list:
            total_expense_amount += expense.amount
        for income in income_list:
            total_income_amount += income.amount
        print(total_income_amount)
        return self.budget - total_expense_amount + total_income_amount
    
    def total_transactions(self):
        income_list = Income.objects.filter(project=self)
        expense_list = Expense.objects.filter(project=self)
        return len(expense_list) + len(income_list)

class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(("Date"), default=datetime.date.today)

    class Meta:
        ordering = ('-amount',)

class Income(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'income')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(("Date"), default=datetime.date.today)

    class Meta:
        ordering = ('-amount',)
