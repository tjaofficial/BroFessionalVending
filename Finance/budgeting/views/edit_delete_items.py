from django.shortcuts import get_object_or_404
from ..models import Income, Expense, Budget, Debt, Savings, CreditCard
from ..forms import IncomeForm, ExpenseForm, BudgetForm, DebtForm, SavingsForm, CreditCardForm
from django.shortcuts import render, redirect

# EDIT VIEWS
def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('budgeting_dashboard')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'edit_items/edit_income.html', {'form': form})

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('budgeting_dashboard')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'edit_items/edit_expense.html', {'form': form})

def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budgeting_dashboard')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'edit_items/edit_budget.html', {'form': form})

def edit_debt(request, debt_id):
    debt = get_object_or_404(Debt, id=debt_id, user=request.user)
    if request.method == "POST":
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            form.save()
            return redirect('budgeting_dashboard')
    else:
        form = DebtForm(instance=debt)
    return render(request, 'edit_items/edit_debt.html', {'form': form})

def edit_savings(request, savings_id):
    savings = get_object_or_404(Savings, id=savings_id, user=request.user)
    if request.method == "POST":
        form = SavingsForm(request.POST, instance=savings)
        if form.is_valid():
            form.save()
            return redirect('budgeting_dashboard')
    else:
        form = SavingsForm(instance=savings)
    return render(request, 'edit_items/edit_savings.html', {'form': form})

def edit_credit_card(request, credit_card_id):
    card = get_object_or_404(CreditCard, id=credit_card_id, user=request.user)
    if request.method == "POST":
        form = CreditCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('budgeting_dashboard')
    else:
        form = CreditCardForm(instance=card)
    return render(request, 'edit_items/edit_credit_card.html', {'form': form})

# DELETE VIEWS
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    income.delete()
    return redirect('budgeting_dashboard')

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    return redirect('budgeting_dashboard')

def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    budget.delete()
    return redirect('budgeting_dashboard')

def delete_debt(request, debt_id):
    debt = get_object_or_404(Debt, id=debt_id, user=request.user)
    debt.delete()
    return redirect('budgeting_dashboard')

def delete_savings(request, savings_id):
    savings = get_object_or_404(Savings, id=savings_id, user=request.user)
    savings.delete()
    return redirect('budgeting_dashboard')

def delete_credit_card(request, credit_card_id):
    card = get_object_or_404(CreditCard, id=credit_card_id, user=request.user)
    card.delete()
    return redirect('budgeting_dashboard')
