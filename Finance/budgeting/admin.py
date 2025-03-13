from django.contrib import admin
from .models import *
from .ai_categorizer import train_categorization_model
from django.shortcuts import redirect
from django.contrib import messages

# Register your models here.

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Budget)
admin.site.register(Debt)
admin.site.register(Savings)
admin.site.register(CreditCard)
admin.site.register(Bill)
admin.site.register(UserProfile)

@admin.action(description="Train AI Model for Categorization")
def train_model_action(modeladmin, request, queryset):
    train_categorization_model()
    messages.success(request, "✅ AI Model Trained Successfully!")
    return redirect("admin:budgeting_transaction_changelist")

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "category", "ai_predicted_category", "date")
    actions = [train_model_action]  # ✅ Adds training option in Django admin

admin.site.register(Transaction, TransactionAdmin)