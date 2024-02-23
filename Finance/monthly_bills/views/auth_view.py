from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('vendDash')
        else:
            return redirect('login')
    else:
        return render(request, 'landing/login.html',{})
    

def logout_view(request):
    logout(request)
    return redirect('login')
    