from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from ..models import machine_build_model, home_inventory_model, item_data_model, item_stock_model, inventory_sheets_model, LossStockModel
from ..forms import item_data_form, item_stock_form, LossStockForm
from ..utils import find_machines_with_item
import datetime
from django.contrib.auth.decorators import login_required
import json
from django.db.models import OuterRef, Subquery
from django.db import models
from django.http import JsonResponse 
from django.db.models import Sum, F
from django.db.models.functions import Cast

lock = login_required(login_url='login')

@lock
def view_snacks_view(request):
    itemDatabase = item_data_model.objects.all().order_by('itemID')
    stockDatabase = item_stock_model.objects.all().order_by('-date_updated')
    inventoryQuery = inventory_sheets_model.objects.all()
    snackStockList = []

    # Get the latest stock entry per item (if available)
    latest_stock = (
        item_stock_model.objects
        .filter(itemChoice=OuterRef('pk'))
        .order_by('-date_updated')  # Get the most recent stock entry
    )
    latest_qty = (
        home_inventory_model.objects
        .filter(item=OuterRef('pk'))
        .values('quantity')[:1]
    )
    # Query all items, attaching latest stock details (or default values)
    inventory = item_data_model.objects.annotate(
        latest_qty=Subquery(latest_qty, output_field=models.IntegerField()),
        latest_exp_date=Subquery(latest_stock.values('exp_date')[:1], output_field=models.DateField())
    ).order_by('itemPrimaryType', 'itemSecondaryType', 'itemID')
    print(inventory.values()[0])



    # Organizing data into a structured format
    categorized_inventory = {}
    for item in inventory:
        primary_type = item.itemPrimaryType
        secondary_type = item.itemSecondaryType

        if primary_type not in categorized_inventory:
            categorized_inventory[primary_type] = {}

        if secondary_type not in categorized_inventory[primary_type]:
            categorized_inventory[primary_type][secondary_type] = []
        
        if item not in categorized_inventory[primary_type][secondary_type]:
            categorized_inventory[primary_type][secondary_type].append(item)

    newShit = item_data_model.objects.all().order_by('itemID')
    newShit = newShit.filter(itemPrimaryType="drinks")
    print(categorized_inventory)
    
    return render(request, 'snacks/view_snacks.html',{
        'itemDatabase': itemDatabase, 
        'stockDatabase': stockDatabase,
        'snackStockList': snackStockList,
        'categorized_inventory': categorized_inventory
    })
    
def view_individual_snack_view(request, itemID):
    item_data_query = item_data_model.objects.get(itemID=itemID)
    item_stock_query = (
        item_stock_model.objects
        .filter(itemChoice__itemID=itemID)
        .order_by("-date_updated")  # Order by most recent first
        .annotate(total_cost=F("qty_of_units") * F("cost_per_unit"))  # Multiply fields
    )

    if request.method == "POST":
        form = LossStockForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to same page
    else:
        initial_data = {
            'reported_by': request.user.first_name + " " + request.user.last_name,
        }
        form = LossStockForm(
            initial=initial_data,
            itemID=itemID
        )
    machines_with_item = find_machines_with_item(itemID)
    print(f"DEBUG: Machines with {itemID}: {machines_with_item}")  # Debugging print statement
    return render(request, 'snacks/view_individual_snack.html',{
        'item': item_data_query,
        'machines': machines_with_item,
        'transactions': item_stock_query,
        "theLossForm": form

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
            A = formData.save()
            at_home_stock_for_item = home_inventory_model.objects.get(item__itemID=itemID)
            change = int(A.qty_per_unit) * int(A.qty_of_units)
            at_home_stock_for_item.update_stock(change, "Restocked")
            return redirect('view_snacks')
    return render(request, 'snacks/add_stock.html',{
        'snackDataForm': form
    })

def get_statistics(request):
    # Extract parameters from the request
    timeframe = request.GET.get("timeframe", "alltime")
    selected_option = request.GET.get("selectedOption", None)
    machine = request.GET.get("machine", "all")
    itemID = request.GET['itemID']
    year = request.GET.get("year", None)
    print(request.GET)
    # Define a filter dictionary
    filters = {}

    # Get the current date
    today = datetime.date.today()

    # Timeframe filtering
    if selected_option:
        year = int(year.replace("year", ""))
        if timeframe == "monthly":
                month = int(selected_option.replace("month", ""))  # Extract month number
                filters["date__year"] = year # Use correct year filtering
                filters["date__month"] = month
        elif timeframe == "annual":
            if year:
                filters["date__year"] = year

    # Apply machine filtering
    if machine != "all":
        filters["id_tag__id_tag"] = machine

    # Get the correct time range
    today = datetime.date.today()
    if timeframe == "weekly":
        start_date = today - datetime.timedelta(days=today.weekday())  # Start of the week
    elif timeframe == "monthly":
        start_date = datetime.date(today.year, int(selected_option.replace("month", "")), 1)
    elif timeframe == "annual":
        start_date = datetime.date(int(selected_option.replace("year", "")), 1, 1)
    else:
        start_date = datetime.date(2022, 1, 1)  # All-time data since 2022

    filters["date__gte"] = start_date  # Filter transactions from this date onward

    print(f"DEBUG: Filters applied: {filters}")  # Debugging statement

    # Process total cost, revenue, sold items, etc.
    machines_with_item = find_machines_with_item(itemID)
    print(machines_with_item)
    total_sold = 0
    total_revenue = 0
    total_loss_qty = 0
    total_loss = 0
    # Query all relevant inventory records
    
    inventory_records = inventory_sheets_model.objects.filter(**filters)
 
    sales_data_dict = {}  # Dictionary to track sales by date

    for record in inventory_records:
        try:
            record_data = record.data  # JSONField (already a dict)

            # Get only the lanes that contain the specific item
            relevant_lanes = [m["lane"] for m in machines_with_item if m["machine"] == record.id_tag.id_tag]

            for lane in relevant_lanes:
                if lane in record_data:  # Check if this lane exists in record_data
                    sold_qty = int(record_data[lane].get("sold", 0))  # Get sold value for this lane
                    sold_price = float(next(m["cost"] for m in machines_with_item if m["lane"] == lane and m["machine"] == record.id_tag.id_tag))
                    loss_qty = int(record_data[lane].get("removed", 0))

                    total_revenue += (sold_price * sold_qty)
                    total_sold += sold_qty
                    total_loss_qty += loss_qty
                    total_loss += (sold_price * loss_qty)

                    record_date = str(record.date)  # Convert date to string
                
                    # If date exists, update the values
                    if record_date in sales_data_dict:
                        sales_data_dict[record_date]["sold"] += sold_qty
                        sales_data_dict[record_date]["amount"] += (sold_price * sold_qty)
                    else:
                        sales_data_dict[record_date] = {
                            "date": record_date,
                            "sold": sold_qty,
                            "amount": (sold_price * sold_qty)
                        }
        except (json.JSONDecodeError, KeyError, ValueError):
            continue  # Skip malformed data
    sales_data = list(sales_data_dict.values())
    # Total Cost Query and Calc
    filters2 = {'date_updated'+ k[4:] if k[:4] == 'date' else k: v for k, v in filters.items() if k in ["date_updated", "exp_date", "itemChoice"]}
    print(filters2)
    total_cost = (
        item_stock_model.objects
        .filter(itemChoice__itemID=itemID, **filters2)
        .annotate(product=F('cost_per_unit') * F('qty_of_units'))
        .aggregate(total=Sum('product'))['total'] or 0
    )

    total_bought = (
        item_stock_model.objects
        .filter(itemChoice__itemID=itemID, **filters2)
        .annotate(product=F('qty_per_unit') * F('qty_of_units'))
        .aggregate(total=Sum('product'))['total'] or 0
    )

    # Query the database
    data = inventory_sheets_model.objects.filter(**filters).aggregate(
        #total_sold=Sum("data__sold"),  # Assuming `data` field stores JSON where `sold` exists
        total_revenue=Sum("collected"),  # Modify this if revenue is calculated differently
        total_loss=Sum("data__removed"),  # Modify this based on how you define losses
    )
    
    

    # Get sales data
    # sales_data = (
    #     inventory_records
    #     .values("date")
    #     .annotate(sold=Sum("data__sold"))
    #     .order_by("date")
    # )
    print(list(sales_data))
    response_data = {
        "totalCost": total_cost or 0,
        "totalSold": total_sold or 0,
        "totalRevenue": total_revenue or 0,
        "totalLoss": -(total_loss) or 0,
        "totalBought": total_bought or 0,
        "sales_over_time": list(sales_data),
        "totalLoss_qty": total_loss_qty or 0
    }

    return JsonResponse(response_data)





