from django.shortcuts import render, redirect
from ..models import item_data_model, item_stock_model, inventory_sheets_model
from ..forms import item_data_form, item_stock_form
import datetime
from django.contrib.auth.decorators import login_required
import json
lock = login_required(login_url='login')

@lock
def view_snacks_view(request):
    itemDatabase = item_data_model.objects.all()
    stockDatabase = item_stock_model.objects.all().order_by('-date_updated')
    inventoryQuery = inventory_sheets_model.objects.all()
    snackStockList = []
    for snack in itemDatabase:
        print(snack)
        match = False
        addingStock = 0
        closestExp = 'n/a'
        for stock in stockDatabase:
            if stock.itemChoice == snack:
                match = True
                #break
                addingStock += stock.qty_per_unit
                if closestExp == 'n/a' or closestExp > stock.exp_date:
                    closestExp = stock.exp_date
        addedToMachine = 0
        for inventory in inventoryQuery:
            machineLayout = json.loads(inventory.data)
            for x in machineLayout:
                itemName = machineLayout[x][0]['item_name']
                itemsAdded = int(machineLayout[x][4]['added'])
                if itemName == snack.name:
                    addedToMachine += itemsAdded
        stockLeft = addingStock - addedToMachine
        snackStockList.append((snack, stockLeft, closestExp))
        print(match)
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