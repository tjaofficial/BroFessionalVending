from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..models import UserProfile

def login_view(request):
    if request.method == "POST":
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            business = UserProfile.objects.get(user=request.user).business_type
            if business == "Vending":
                return redirect('vendDash')
            elif business == "Legacy":
                return redirect('admin_dash')
            elif business == "Tenant":
                return redirect('tenant_dashboard')
        else:
            return redirect('login')
    else:
        return render(request, 'landing/login.html',{})
    

def logout_view(request):
    logout(request)
    return redirect('login')
    