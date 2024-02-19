from django.shortcuts import render, redirect
from ..models import bill_items_model, pay_log, income_log, purchase_model, bills_model, vending_finance, inventory_sheets_model
from ..forms import pay_log_form, add_purchase_form, add_bills_form, income_log_form, vending_finance_form
import datetime
import calendar
import json

def createBillDate(theDay):
    today = datetime.date.today()
    date = str(today.year) + '-' 
    month = str(today.month)
    theDay = str(theDay)
    if len(month) < 2:
        month = '0' + month
    if len(theDay) < 2:
        theDay = '0' + str(theDay)
    date += month + '-' + theDay
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    return date
    

def monthly_bills(request, year, month):
    today = datetime.date.today()
    if int(month) == 1:
        prev_year = str(int(year) - 1)
    else:
        prev_year = year
    if 1 < int(month) <= 12:
        prev_month = str(int(month)-1)
    else:
        prev_month = str(12)
        
    if int(month) == 12:
        next_year = str(int(year) + 1)
    else:
        next_year = year
    if 1 <= int(month) < 12:
        next_month = str(int(month)+1)
    else:
        next_month = str(1)
    
    monthList = [int(month), calendar.month_name[int(month)], int(year), calendar.month_name[int(month)][:3]]
    billModel = bills_model.objects.all().filter(start_date__year=int(year))
    
    monthlyBills = []
    firstHalfBills = []
    secondHalfBills = []
    monthlyBillsDataList = {}
    
    for bill in billModel:
        if bill.stop_date:
            print('CHECK 1')
            if bill.start_date.month <= monthList[0] <= bill.stop_date.month:
                print('CHECK 2')
                monthlyBills.append(bill)
                if bill.charge_day_1 >= 15:
                    date = year + '-' + month + '-' + str(bill.charge_day_1)
                    print('CHECK 3.1')
                    secondHalfBills.append(bill)
                    try:
                        monthlyBillsDataList[bill.title + '-' + str(datetime.datetime.strptime(date, "%Y-%m-%d").date())]=[bill.title, str(datetime.datetime.strptime(date, "%Y-%m-%d").date()), str(bill.budget_amt)]
                    except ValueError as e:
                        lastDay = calendar.monthrange(monthList[2], monthList[0])[1]
                        date = year + '-' + month + '-' + str(lastDay)
                        monthlyBillsDataList[bill.title + str(datetime.datetime.strptime(date, "%Y-%m-%d").date())]=[bill.title, str(datetime.datetime.strptime(date, "%Y-%m-%d").date()), str(bill.budget_amt)]
                elif bill.charge_day_1 < 15:
                    date = year + '-' + month + '-' + str(bill.charge_day_1)
                    print('CHECK 3.2')
                    firstHalfBills.append(bill)
                    monthlyBillsDataList[bill.title + str(datetime.datetime.strptime(date, "%Y-%m-%d").date())]=[bill.title, str(datetime.datetime.strptime(date, "%Y-%m-%d").date()), str(bill.budget_amt)]
                    if bill.billing_period.lower() == 'bi-monthly':
                        date2 = year + '-' + month + '-' + str(bill.charge_day_2)
                        print('CHECK 4')
                        secondHalfBills.append(bill)
                        monthlyBills.append(bill)
                        monthlyBillsDataList[bill.title + '-' + str(datetime.datetime.strptime(date, "%Y-%m-%d").date())]=[bill.title, str(datetime.datetime.strptime(date2, "%Y-%m-%d").date()), str(bill.budget_amt)]
        else:
            print('CHECK 1.1')
            if bill.start_date.month <= monthList[0]:
                monthlyBills.append(bill)
                if bill.charge_day_1 >= 15:
                    date = year + '-' + month + '-' + str(bill.charge_day_1)
                    print('CHECK 5.1')
                    secondHalfBills.append(bill)
                    try:
                        monthlyBillsDataList[bill.title + '-' + str(datetime.datetime.strptime(date, "%Y-%m-%d").date())]=[bill.title, str(datetime.datetime.strptime(date, "%Y-%m-%d").date()), str(bill.budget_amt)]
                    except ValueError as e:
                        lastDay = calendar.monthrange(monthList[2], monthList[0])[1]
                        date = year + '-' + month + '-' + str(lastDay)
                        monthlyBillsDataList[bill.title + '-' + str(datetime.datetime.strptime(date, "%Y-%m-%d").date())]=[bill.title, str(datetime.datetime.strptime(date, "%Y-%m-%d").date()), str(bill.budget_amt)]
                elif bill.charge_day_1 < 15:
                    date = year + '-' + month + '-' + str(bill.charge_day_1)
                    print('CHECK 5.2')
                    firstHalfBills.append(bill)
                    monthlyBillsDataList[bill.title + '-' + str(datetime.datetime.strptime(date, "%Y-%m-%d").date())]=[bill.title, str(datetime.datetime.strptime(date, "%Y-%m-%d").date()), str(bill.budget_amt)]
                    if bill.billing_period.lower() == 'bi-monthly':
                        date2 = year + '-' + month + '-' + str(bill.charge_day_2)
                        print('CHECK 6')
                        secondHalfBills.append(bill)
                        monthlyBills.append(bill)
                        monthlyBillsDataList[bill.title + '-' + str(datetime.datetime.strptime(date, "%Y-%m-%d").date())]=[bill.title, str(datetime.datetime.strptime(date2, "%Y-%m-%d").date()), str(bill.budget_amt)]
                
    monthlyBillsDataList = json.dumps(monthlyBillsDataList)
    print(monthlyBillsDataList)
    payments = pay_log_form
    payment_model = pay_log.objects.all().filter(date__year=today.year, date__month=monthList[0]).order_by('date')
    income_data = income_log.objects.all().filter(date__year=today.year, date__month=monthList[0]).order_by('date')
    purchase_data = purchase_model.objects.all().filter(date__year=today.year, date__month=monthList[0]).order_by('date')

    last_months_2nd_check = 0.00
    this_months_1st_check = 0.00
    expense = 0.00
    music = 0.00
    extra = 0.00   

            
    for x in income_data:
        if x.title == 'first':
            last_months_2nd_check = x.amount
        elif x.title == 'second':
            this_months_1st_check = x.amount   
        elif x.title == 'expense':
            expense = x.amount
        elif x.title == 'music':
            music = x.amount
        elif x.title == 'extra':
            extra = x.amount
            
    purchase_1st = []
    purchase_2nd = []
    purchase_this_month=[]
    for x in purchase_data:
        if int(x.date.day) < 15:
            purchase_1st.append(x)
            purchase_this_month.append(x)
        else:
            purchase_2nd.append(x)
            purchase_this_month.append(x)
    
    whole_month_bills = []
        
    total_income = float(last_months_2nd_check) + float(this_months_1st_check) + float(expense) + float(music) + float(extra)
    
    totals = []
    
    A = []
    B = []
    C = []
    D = []
    
    for bill_1st in firstHalfBills:
        A.append(bill_1st.budget_amt)
    for bill_2nd in secondHalfBills:
        B.append(bill_2nd.budget_amt)
    for payments_list1 in payment_model:
        if payments_list1.date.day < 15:
            C.append(payments_list1.payment)
    for purchases in purchase_data:
        if purchases.date.day < 15:
            C.append(purchases.amount)
    for payments_list2 in payment_model:
        if payments_list2.date.day >= 15:
            D.append(payments_list2.payment)
    for purchases2 in purchase_data:
        if purchases2.date.day >= 15:
            D.append(purchases2.amount)
        
    totals.append(sum(A))
    totals.append(sum(B))
    totals.append(sum(C))
    totals.append(sum(D))
    
    monthTotalBills = totals[0] + totals[1]
    monthTotalSpend = totals[2] + totals[3]
    
    totals.append(monthTotalBills)
    totals.append(monthTotalSpend)
    # totals[0] - bill total for first 2 weeks
    # totals[1] - bill total for last 2 weeks
    # totals[2] - spend total for first 2 weeks
    # totals[3] - spend total for last 2 weeks
    # totals[4] - total monthly bills
    # totals[5] - total monthly spending
    
    if request.method == 'POST':
        form_data = pay_log_form(request.POST)
        if form_data.is_valid():
            form_data.save()
            
            return redirect ('monthly_bills', year, month)
        
    return render (request,'monthly_bills_layout.html',{
        'purchase_data': purchase_this_month, 
        'first_half_bills' : firstHalfBills, 
        'second_half_bills': secondHalfBills,
        'totals': totals,
        'today': today, 
        'payments': payments, 
        'payment_model': payment_model, 
        'last_months_2nd_check': last_months_2nd_check, 
        'this_months_1st_check': this_months_1st_check, 
        'expense': expense, 
        'music': music, 
        'total_income': total_income, 
        'extra': extra, 
        'purchase_data_1': purchase_1st, 
        'purchase_data_2': purchase_2nd,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'monthList': monthList,
        'monthlyBillsDataList': monthlyBillsDataList,
    })
    
def add_bills(request):
    form = add_bills_form
    today = datetime.date.today()
    
    if request.method == "POST":
        form_data = form(request.POST)
        if form_data.is_valid():
            form_data.save()
            
            return redirect ('monthly_bills', today.year, today.month)
    
    
    return render (request, 'add_bill_item.html', {
        'form': form,
    })
  
def add_income(request):
    form = income_log_form
    today = datetime.date.today()
    
    if request.method == "POST":
        form_data = form(request.POST)
        if form_data.is_valid():
            form_data.save()
            
            return redirect ('monthly_bills', today.year, today.month)
    
    return render (request, 'add_income.html', {
        'form': form,
    })

def add_purchase(request):
    form = add_purchase_form
    
    if request.method == "POST":
        form_data = form(request.POST)
        if form_data.is_valid():
            form_data.save()
            
            return redirect ('monthly_bills')
    
    return render (request, 'add_purchase.html', {
        'form': form,
    })

def vending_finances(request, year, month):
    today = datetime.date.today()
    if int(month) == 1:
        prev_year = str(int(year) - 1)
    else:
        prev_year = year
    if 1 < int(month) <= 12:
        prev_month = str(int(month)-1)
    else:
        prev_month = str(12)
        
    if int(month) == 12:
        next_year = str(int(year) + 1)
    else:
        next_year = year
    if 1 <= int(month) < 12:
        next_month = str(int(month)+1)
    else:
        next_month = str(1)
    
    monthList = [int(month), calendar.month_name[int(month)], int(year), calendar.month_name[int(month)][:3]]
    billModel = vending_finance.objects.all().filter(date__year=int(year), date__month=int(month)).order_by('date')
    
    monthlyTrans = []
    totalDeposit = []
    totalwithdrawal = []
    for trans in billModel:
        if trans.withdrawal:
            monthlyTrans.append((True, trans))
        elif trans.deposit:
            monthlyTrans.append((False, trans))

        if trans.deposit:
            totalDeposit.append(trans.deposit)
        else:
            totalwithdrawal.append(trans.withdrawal)

    vendingForm = vending_finance_form
    
    totalD = 0
    for d in totalDeposit:
        totalD += d
        
    totalW = 0
    for w in totalwithdrawal:
        totalW += w
        
    if request.method == 'POST':
        dataCopy = request.POST.copy()
        if request.POST['type'] == 'withdrawal':
            dataCopy['withdrawal'] = request.POST['amount']
        else:
            dataCopy['deposit'] = request.POST['amount']
            
        print(dataCopy)
        form_data = vending_finance_form(dataCopy)
        print(form_data.errors)
        if form_data.is_valid():
            form_data.save()

            return redirect ('vendingFinances', year, month)
        
    return render (request,'vending_finances.html',{
        'today': today, 
        'vendingForm': vendingForm, 
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'monthList': monthList,
        'monthlyTrans': monthlyTrans,
        'totalD': totalD,
        'totalW': totalW,
    })