from django.shortcuts import render, redirect
from ..forms import gas_log_form, mileage_log_form
from ..models import gas_log_model, mileage_log_model
import datetime


def gas_log(request):
    existingG = False
    existingM = False
    today = datetime.date.today()
    gas = gas_log_model.objects.all()
    mileage = mileage_log_model.objects.all()
    totalM=''
    taxDm=''
    totalG=''
    taxDg=''
    if len(gas) > 0:
        existingG = True
    if len(mileage) > 0:
        existingM = True
    
    if existingM:
        totalM = 0
        for logM in mileage:
            totalM += logM.mileage
            
        taxDm = round((totalM * .625), 2)
    
    if existingG:
        totalG = 0
        for logG in gas:
            totalG += logG.actual_cost
            
        taxDg = round((totalG * .5), 2)
        
    
    return render (request,'gas_log.html',{
        'gas': gas, 'existingG': existingG, 'existingM': existingM, 'mileage': mileage, 'totalM': totalM, 'taxDm': taxDm, 'totalG': totalG, 'taxDg': taxDg
    })
    
    
def add_gas_log(request):
    today = datetime.date.today()
    initial_data = {
        'date': today
    }
    form = gas_log_form(initial=initial_data)
    if request.method == 'POST':
        form = gas_log_form(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('gasLog')
            
    
    return render (request,'add_gas_log.html',{
        'form': form
    })
    
def add_mileage_log(request):
    today = datetime.date.today()
    initial_data = {
        'date': today
    }
    form = mileage_log_form(initial=initial_data)
    if request.method == 'POST':
        form = mileage_log_form(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('gasLog')
    
    return render (request,'add_mileage_log.html',{
        'form': form
    })