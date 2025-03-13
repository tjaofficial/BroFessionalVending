from django.shortcuts import render
from ..models import Transaction

def transactions_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, "transactions.html", {"transactions": transactions})
