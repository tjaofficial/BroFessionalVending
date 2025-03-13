from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from ..models import Transaction
from ..ai_categorizer import train_categorization_model

def approve_ai_prediction(request, transaction_id):
    """ User approves AI prediction """
    if request.method == "POST":
        transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
        transaction.category = transaction.ai_predicted_category  # ✅ Assign AI category
        transaction.ai_approved = True  # ✅ Mark as approved
        transaction.save()
        messages.success(request, "✅ AI prediction approved!")
    return redirect("budgeting_dashboard")

def correct_ai_prediction(request, transaction_id):
    """ User corrects AI prediction and improves the model """
    if request.method == "POST":
        corrected_category = request.POST.get("corrected_category")
        transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
        transaction.category = corrected_category  # ✅ Assign corrected category
        transaction.ai_approved = True  # ✅ Mark as manually corrected
        transaction.save()

        messages.success(request, f"✏ AI prediction corrected to {corrected_category}!")
        train_categorization_model()  # ✅ Retrain model with new data
    return redirect("budgeting_dashboard")
