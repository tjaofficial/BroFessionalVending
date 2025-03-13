from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', budgeting_dashboard, name='budgeting_dashboard'),
    path('add-income/', add_income, name='add_income'),
    path('add-expense/', add_expense, name='add_expense'),
    path('add-budget/', add_budget, name='add_budget'),
    path('add-debt/', add_debt, name='add_debt'),
    path('add-savings/', add_savings, name='add_savings'),
    path('add-credit-card/', add_credit_card, name='add_credit_card'),

    path('edit-income/<int:income_id>/', edit_income, name='edit_income'),
    path('edit-expense/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('edit-budget/<int:budget_id>/', edit_budget, name='edit_budget'),
    path('edit-debt/<int:debt_id>/', edit_debt, name='edit_debt'),
    path('edit-savings/<int:savings_id>/', edit_savings, name='edit_savings'),
    path('edit-credit-card/<int:credit_card_id>/', edit_credit_card, name='edit_credit_card'),

    path('delete-income/<int:income_id>/', delete_income, name='delete_income'),
    path('delete-expense/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('delete-budget/<int:budget_id>/', delete_budget, name='delete_budget'),
    path('delete-debt/<int:debt_id>/', delete_debt, name='delete_debt'),
    path('delete-savings/<int:savings_id>/', delete_savings, name='delete_savings'),
    path('delete-credit-card/<int:credit_card_id>/', delete_credit_card, name='delete_credit_card'),

    path('add-bill/', add_bill, name='add_bill'),
    path('edit-bill/<int:bill_id>/', edit_bill, name='edit_bill'),
    path('delete-bill/<int:bill_id>/', delete_bill, name='delete_bill'),

    path('reports/', financial_reports, name='financial_reports'),

    path('connect-bank/', connect_bank, name='connect_bank'),
    path('fetch-transactions/', fetch_transactions, name='fetch_transactions'),
    path('exchange-token/', exchange_public_token, name='exchange_token'),

    path('transactions/', transactions_view, name='transactions'),
    path("dismiss-alert/<int:transaction_id>/", dismiss_transaction_alert, name="dismiss_transaction_alert"),
    path("update-alert-threshold/", update_alert_threshold, name="update_alert_threshold"),
    path("update-category-threshold/", update_category_threshold, name="update_category_threshold"),

    path("approve-ai/<int:transaction_id>/", approve_ai_prediction, name="approve_ai_prediction"),
    path("correct-ai/<int:transaction_id>/", correct_ai_prediction, name="correct_ai_prediction"),


    path("download/pdf/", download_pdf_report, name="download_pdf_report"),
    path("download/csv/", download_csv_report, name="download_csv_report"),
]
