from django.shortcuts import render, redirect
from ..models import Income, Expense, Budget, Debt, Savings, CreditCard
from ..forms import IncomeForm, ExpenseForm, BudgetForm, DebtForm, SavingsForm, CreditCardForm

def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Assign current user
            income.save()
            return redirect('budgeting_dashboard')
    else:
        form = IncomeForm()
    return render(request, 'add_items/add_income.html', {'form': form})

def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            budget = Budget.objects.filter(user=request.user, category=expense.description.lower()).first()
            print(budget)
            if budget:
                print('check1')
                budget.current_spending += expense.amount
                budget.save()
                print(budget)
            return redirect('budgeting_dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'add_items/add_expense.html', {'form': form})

def add_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('budgeting_dashboard')
    else:
        form = BudgetForm()
    return render(request, 'add_items/add_budget.html', {'form': form})

def add_debt(request):
    if request.method == "POST":
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.user = request.user
            debt.save()
            return redirect('budgeting_dashboard')
    else:
        form = DebtForm()
    return render(request, 'add_items/add_debt.html', {'form': form})

def add_savings(request):
    if request.method == "POST":
        form = SavingsForm(request.POST)
        if form.is_valid():
            savings = form.save(commit=False)
            savings.user = request.user
            savings.save()
            return redirect('budgeting_dashboard')
    else:
        form = SavingsForm()
    return render(request, 'add_items/add_savings.html', {'form': form})

def add_credit_card(request):
    if request.method == "POST":
        form = CreditCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('budgeting_dashboard')
    else:
        form = CreditCardForm()
    return render(request, 'add_items/add_credit_card.html', {'form': form})
