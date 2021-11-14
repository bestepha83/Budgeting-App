from django.test import TestCase

from .models import Project, Expense, Income


class QuestionModelTests(TestCase):


    def total_spent_info(self):
        # project = Project.objects.all()
        expenses = Expense.objects.all()
        income = Income.objects.all()
        finalrep = {}

        # def get_budget(project):
        #     return project.budget

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
        
        # finalrep["project"] = get_budget(project)
        finalrep["expenses"] = get_expenses(expenses)
        finalrep["income"] = get_income(income)
        self.assertIs('total_spent_info', False)
