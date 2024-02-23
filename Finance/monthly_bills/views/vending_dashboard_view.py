from django.shortcuts import render
from django.contrib.auth.decorators import login_required
lock = login_required(login_url='login')

@lock
def vending_dashboard(request):
    
    
    
    
    return render (request,'vending_dashboard.html',{
        
    })