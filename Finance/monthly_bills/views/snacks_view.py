from django.shortcuts import render, redirect
from ..models import item_data_model, item_stock_model
from ..forms import item_data_form, item_stock_form
import datetime
from django.contrib.auth.decorators import login_required
lock = login_required(login_url='login')

@lock
def view_snacks_view(request):
    itemDatabase = item_data_model.objects.all()
    stockDatabase = item_stock_model.objects.all().order_by('-date_updated')

    snackStockList = []
    for snack in itemDatabase:
        match = False
        for stock in stockDatabase:
            if stock.itemChoice == snack:
                match = True
                snackStockList.append((snack, stock))
                break
        if not match:
            snackStockList.append((snack, False))
                
    print(snackStockList)
    
    
    return render(request, 'snacks/view_snacks.html',{
        'itemDatabase': itemDatabase, 
        'stockDatabase': stockDatabase,
        'snackStockList': snackStockList
    })
    

@lock
def add_snack_view(request):
    
    if request.method == "POST":
        data = request.POST
        formData = item_data_form(data)
        if formData.is_valid():
            formData.save()
            return redirect('view_snacks')
    return render(request, 'snacks/add_snack.html',{
        "snackForm": item_data_form,
        'snackDataForm': item_stock_form
    })
   
@lock 
def add_stock_view(request, itemID):
    today = datetime.datetime.today().date()
    snackData = item_data_model.objects.get(itemID=itemID)
    initial_data = {
        'itemChoice': snackData,
        'date_updated': today
    }
    form = item_stock_form(initial=initial_data)
    if request.method == "POST":
        data = request.POST
        formData = item_stock_form(data)
        if formData.is_valid():
            formData.save()
            return redirect('view_snacks')
    return render(request, 'snacks/add_stock.html',{
        'snackDataForm': form
    })