from django.shortcuts import render, redirect
from ..models import Income, Bill, Expense, Budget, Debt, Savings, CreditCard, Transaction, UserProfile
import json
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum
from django.http import JsonResponse
from collections import defaultdict
from ..ai_categorizer import predict_category, train_categorization_model, evaluate_model_accuracy

def budgeting_dashboard(request):
    user = request.user  # Get the logged-in user

    # Fetch user-specific financial data
    total_income = sum(income.amount for income in Income.objects.filter(user=user))
    total_expenses = sum(expense.amount for expense in Expense.objects.filter(user=user))
    net_savings = total_income - total_expenses

    incomes = Income.objects.filter(user=user)
    expenses = Expense.objects.filter(user=user)
    budgets = Budget.objects.filter(user=user)
    debts = Debt.objects.filter(user=user)
    savings = Savings.objects.filter(user=user)
    credit_cards = CreditCard.objects.filter(user=user)
    bills = Bill.objects.filter(user=user).order_by('due_date')

    # Expense Breakdown by Category for Pie Chart
    expense_categories = list(Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount')))
    expense_labels = [item['category'] for item in expense_categories]
    expense_values = [float(item['total']) for item in expense_categories]

    # Budget Progress for Bar Chart
    budget_labels = [budget.category for budget in budgets]
    budget_values = [float(budget.current_spending) for budget in budgets]
    budget_limits = [float(budget.limit) for budget in budgets]

    """ Fetch financial data and highlight large transactions """
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # ✅ Fetch transactions that exceed category-specific or global thresholds
    large_transactions = []
    for txn in Transaction.objects.filter(user=request.user, dismissed=False):
        txn_threshold = profile.get_threshold_for_category(txn.category)
        if txn.amount > txn_threshold:
            large_transactions.append(txn)

    """ Fetch financial data and calculate spending per category & month """
    
    transactions = Transaction.objects.filter(user=request.user)
    
    # ✅ Group transactions by category
    category_totals = defaultdict(float)
    for txn in transactions:
        category_totals[txn.category] += float(txn.amount)

    category_labels = list(category_totals.keys())
    category_values = list(category_totals.values())

    # ✅ Group transactions by month
    monthly_spending = transactions.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')

    month_labels = [entry['month'].strftime('%b %Y') for entry in monthly_spending]
    month_values = [float(entry['total']) for entry in monthly_spending]


    """ Auto-categorize transactions and show financial data """

    transactions = Transaction.objects.filter(user=request.user)

    for txn in transactions:
        if not txn.category:
            predicted = predict_category(txn.name, txn.amount)
            if predicted:
                txn.ai_predicted_category = predicted  # ✅ Store AI prediction
                txn.save()

    """ Auto-categorize transactions and store confidence levels """

    transactions = Transaction.objects.filter(user=request.user)

    for txn in transactions:
        if not txn.category:  # Only predict if no manual category exists
            predicted, confidence = predict_category(txn.name, txn.amount)
            if predicted:
                txn.ai_predicted_category = predicted
                txn.ai_accuracy = round(confidence * 100, 2)  # ✅ Store confidence as percentage
                txn.save()

    """ Auto-categorize transactions and show AI accuracy """

    transactions = Transaction.objects.filter(user=request.user)
    ai_accuracy = evaluate_model_accuracy()

    context = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
        "budgets": budgets,
        "debts": debts,
        "bills": bills,
        "savings": savings,
        "credit_cards": credit_cards,
        "incomes": incomes,
        "expenses": expenses,
        "expense_labels": json.dumps(expense_labels),
        "expense_values": json.dumps(expense_values),
        "budget_labels": json.dumps(budget_labels),
        "budget_values": json.dumps(budget_values),
        "budget_limits": json.dumps(budget_limits),
        "large_transactions": large_transactions,
        "global_threshold": profile.alert_threshold,
        "category_thresholds": profile.category_thresholds or {},
        "transactions": transactions,
        "category_labels": json.dumps(category_labels),
        "category_values": json.dumps(category_values),
        "month_labels": json.dumps(month_labels),
        "month_values": json.dumps(month_values),
        "ai_accuracy": ai_accuracy,
    }
    
    return render(request, "budget_dash.html", context)

def dismiss_transaction_alert(request, transaction_id):
    """ API to dismiss a transaction alert """
    if request.method == "POST":
        transaction = Transaction.objects.filter(id=transaction_id, user=request.user).first()
        if transaction:
            transaction.dismissed = True
            transaction.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

def update_alert_threshold(request):
    """ Updates the user's custom alert threshold """
    if request.method == "POST":
        new_threshold = request.POST.get("alert_threshold")
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.alert_threshold = float(new_threshold)
        profile.save()
        messages.success(request, "🔔 Alert threshold updated successfully!")
        return redirect("budgeting_dashboard")

    return JsonResponse({"status": "error"}, status=400)

def update_category_threshold(request):
    """ Updates or edits a user's category-specific alert threshold """
    if request.method == "POST":
        category = request.POST.get("category")
        new_threshold = float(request.POST.get("threshold"))

        profile, created = UserProfile.objects.get_or_create(user=request.user)

        # ✅ Update existing threshold if it exists, otherwise add a new one
        thresholds = profile.category_thresholds or {}
        thresholds[category] = new_threshold  # ✅ Update or set new value
        profile.category_thresholds = thresholds
        profile.save()

        messages.success(request, f"🔔 Alert threshold updated for {category} to ${new_threshold}!")
        return redirect("budgeting_dashboard")

    return JsonResponse({"status": "error"}, status=400)

def train_ai_model(request):
    """ Train AI model with existing transactions """
    train_categorization_model()
    return render(request, "ai/train_model_success.html")


