from django.shortcuts import render
import datetime

def dashboard(request):
    today = datetime.date.today()
    month = today.month
    year = today.year
    
    
    
    return render (request,'dashboard.html',{
        'month': month, 'year': year
    })