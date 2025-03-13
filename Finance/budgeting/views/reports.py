import json
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta, date
from ..models import Expense, Income, Bill, Transaction
from django.shortcuts import render, redirect
import io
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse, FileResponse

def financial_reports(request):
    user = request.user

    # Get income & expenses for current month
    current_month = now().month
    current_year = now().year
    monthly_income = Income.objects.filter(user=user, date_received__month=current_month, date_received__year=current_year).aggregate(total=Sum('amount'))['total'] or 0
    monthly_expenses = Expense.objects.filter(user=user, date__month=current_month, date__year=current_year).aggregate(total=Sum('amount'))['total'] or 0
    net_savings = monthly_income - monthly_expenses

    # Expense breakdown by category (for pie chart)
    expense_categories = Expense.objects.filter(user=user, date__month=current_month, date__year=current_year).values('category').annotate(total=Sum('amount'))
    expense_labels = [item['category'] for item in expense_categories]
    expense_values = [float(item['total']) for item in expense_categories]

    # Income vs Expenses comparison (for bar chart)
    last_6_months = [now() - timedelta(days=30 * i) for i in range(6)]
    income_data = []
    expense_data = []
    months = []
    
    for month in reversed(last_6_months):
        month_name = month.strftime("%B")
        months.append(month_name)
        income_total = Income.objects.filter(user=user, date_received__month=month.month, date_received__year=month.year).aggregate(total=Sum('amount'))['total'] or 0
        expense_total = Expense.objects.filter(user=user, date__month=month.month, date__year=month.year).aggregate(total=Sum('amount'))['total'] or 0
        income_data.append(float(income_total))
        expense_data.append(float(expense_total))

    context = {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "net_savings": net_savings,
        "expense_labels": json.dumps(expense_labels),
        "expense_values": json.dumps(expense_values),
        "months": json.dumps(months),
        "income_data": json.dumps(income_data),
        "expense_data": json.dumps(expense_data),
    }
    
    return render(request, "reports/reports.html", context)


def generate_pdf_report(user):
    """ Generate a PDF report of monthly transactions """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Monthly Financial Report")

    pdf.drawString(200, 750, f"Monthly Financial Report for {user.username}")
    pdf.drawString(200, 735, f"Date: {date.today()}")

    transactions = Transaction.objects.filter(user=user, date__month=date.today().month)
    
    y_position = 700
    for txn in transactions:
        pdf.drawString(100, y_position, f"{txn.date} - {txn.name} - ${txn.amount} ({txn.category})")
        y_position -= 20

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer


def generate_csv_report(user):
    """ Generate a CSV report of monthly transactions """
    buffer = io.StringIO()
    csv_writer = csv.writer(buffer)

    csv_writer.writerow(["Date", "Name", "Amount", "Category"])
    
    transactions = Transaction.objects.filter(user=user, date__month=date.today().month)
    
    for txn in transactions:
        csv_writer.writerow([txn.date, txn.name, txn.amount, txn.category])

    buffer.seek(0)
    return buffer

def download_pdf_report(request):
    """ View to generate & download PDF report """
    buffer = generate_pdf_report(request.user)
    return FileResponse(buffer, as_attachment=True, filename="monthly_report.pdf")

def download_csv_report(request):
    """ View to generate & download CSV report """
    buffer = generate_csv_report(request.user)
    response = HttpResponse(buffer, content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=monthly_report.csv"
    return response