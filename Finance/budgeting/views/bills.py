from django.shortcuts import render, redirect
from ..models import Bill
from ..forms import BillForm
from django.shortcuts import get_object_or_404

def add_bill(request):
    if request.method == "POST":
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            return redirect('budgeting_dashboard')
    else:
        form = BillForm()
    return render(request, 'add_items/add_bill.html', {'form': form})

def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id, user=request.user)
    if request.method == "POST":
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('budgeting_dashboard')
    else:
        form = BillForm(instance=bill)
    return render(request, 'edit_items/edit_bill.html', {'form': form})

def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id, user=request.user)
    bill.delete()
    return redirect('budgeting_dashboard')
