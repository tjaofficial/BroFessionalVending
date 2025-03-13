from django import forms
from .models import Income, Expense, Budget, Debt, Savings, CreditCard, Bill

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date_received', 'category']
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date'})
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date', 'category', 'is_recurring']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit']

class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['creditor', 'balance', 'minimum_payment', 'interest_rate']

class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ['goal_name', 'goal_amount', 'current_amount', 'target_date']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'})
        }

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['card_name', 'balance', 'payment_due_date', 'payment_link']
        widgets = {
            'payment_due_date': forms.DateInput(attrs={'type': 'date'})
        }

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name', 'amount', 'due_date', 'is_recurring', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }
