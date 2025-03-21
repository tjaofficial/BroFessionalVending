from django.shortcuts import render, redirect
from ..models import home_inventory_model, cantaLogs_model, price_model, fleet_model, machine_stock_model, vmax576_model, inventory_sheets_model, machine_build_model, item_data_model, canta_payments_model
from ..forms import cantaLogs_form, machine_stock_form, vmax576_form, inventory_sheets_form, vending_finance_form, canta_payments_form
from ..utils import productName
import datetime
from django.apps import apps
import json
import calendar
from django.contrib.auth.decorators import login_required
lock = login_required(login_url='login')


def inventory(request):
    fleet = fleet_model.objects.all()
    
    if request.method == 'POST':
        print(request.POST['id_tags'])
        for item in fleet:
            if request.POST['id_tags'] == item.id_tag:
                return redirect('machineDash', item.machine_type, item.id_tag)
    return render (request,'inventory.html',{
        'fleet': fleet,
    })
    
def jsonSort(model):
    machineLayout = {}
    for item in model:
        if item.itemID[0] == 'A':
            machineLayout['A' + item.itemID[1:]] = item
        if item.itemID[0] == 'B':
            machineLayout['B' + item.itemID[1:]] = item
        if item.itemID[0] == 'C':
            machineLayout['C' + item.itemID[1:]] = item
        if item.itemID[0] == 'D':
            machineLayout['D' + item.itemID[1:]] = item
    return machineLayout
   
@lock 
def machine_options(request, type, id_tag):
    goBack = 'vendDash'
    dataAll = inventory_sheets_model.objects.filter(id_tag__id_tag__exact=id_tag).order_by('-date')
    machine = fleet_model.objects.filter(id_tag__exact=id_tag)
    cantaModel = canta_payments_model.objects.filter(machineChoice__id_tag=id_tag)
    stockModel = machine_stock_model.objects.filter(id_tag__id_tag__exact=id_tag, discontinued=False).order_by('itemID')
    priceModel = price_model.objects.filter(machine_id=id_tag)
    cantaLogs = cantaLogs_model.objects.filter(id_tag__id_tag__exact=id_tag).order_by('-date')
    showForm = False
    
    fullList = []
    totalCollected = 0.00
    for invenLogs in dataAll:
        fullList.append((invenLogs.date, invenLogs, 'inventory'))
        totalCollected += float(invenLogs.collected)
    for cantaLogs in cantaModel:
        fullList.append((cantaLogs.date, cantaLogs, 'cantalope'))
        totalCollected += float(cantaLogs.gross_revenue)
    sortedAllLogs = sorted(fullList, key=lambda a: a[0], reverse=True)
    
    
    if type == 'vmax576':
        showForm = True
    if machine.exists():
        machine = machine[0]
        machineModel = machine.model.replace('-', '_')
        machineURL = machineModel + '_is'
     
    if vmax576_model.objects.filter(id_tag__id=machine.id).exists():
        inventoryLogs = vmax576_model.objects.filter(id_tag__id=machine.id).order_by('-date')
    else:
        inventoryLogs = []

    return render (request,'machine_options.html',{
        'goBack': goBack,
        'inventoryLogs': inventoryLogs,
        'type': type, 
        'id_tag': id_tag,
        'machineURL': machineURL, 
        'machine': machine,
        'totalCollected': totalCollected,
        'showForm': showForm,
        'dataAll': sortedAllLogs
    })   
    
@lock
def stock(request, type, id_tag):
    stock = machine_stock_model.objects.all().filter(id_tag__id_tag__exact=id_tag)
    
    return render (request,'machine_stock.html',{
        'type': type, 'id_tag': id_tag, 'stock': stock
    })
    
@lock
def add_item(request, type, id_tag, selector):
    model = fleet_model.objects.all().filter(id_tag__exact=id_tag)[0]
    initial_data = {
        'id_tag': model,
    }
    stockForm = machine_stock_form(initial=initial_data)
    

    if request.method == 'POST':
        if selector == 'item':
            form = machine_stock_form(request.POST)
            
        print(form.errors)
        if form.is_valid():
            form.save()
            
            return redirect ('stock', type, id_tag)
    
    
    return render (request,'add_item.html',{
        'selector': selector, 'stockForm': stockForm
    })
   
@lock 
def vmax576_is(request, type, id_tag):
    vmax576_data = vmax576_model.objects.all().order_by('-date')
    if vmax576_data.exists():
        vmax576_oldData = [
            json.dumps(vmax576_data[0].lane_1),
            json.dumps(vmax576_data[0].lane_2),
            json.dumps(vmax576_data[0].lane_3),
            json.dumps(vmax576_data[0].lane_4),
            json.dumps(vmax576_data[0].lane_5),
            json.dumps(vmax576_data[0].lane_6),
            json.dumps(vmax576_data[0].lane_7),
            json.dumps(vmax576_data[0].lane_8),
        ]
    else:
        vmax576_oldData = False
    print(vmax576_oldData)
    
    today = datetime.date.today()
    machine = fleet_model.objects.all().filter(id_tag__exact=id_tag)
    if len(machine) > 0:
        machine = machine[0]
    includeStr = machine.model + '_block.html'
    itemsStocked = machine_stock_model.objects.all().filter(id_tag__id_tag__exact=id_tag, discontinued=False)
    def handleNumberIntEmpty(number):
        if number:
            number = int(number)
        else:
            number = 0
        return number
            
        
# STARTING HERE SPECIFICALLY FOR vmax576-------------
    item_list = []
    for x in itemsStocked:
        item_list.append(x.name)
        
    if len(item_list) != 8:
        diff = 8-len(item_list)
        for numb in range(diff):
            item_list.append('--none--')
        
    
    initial_data = {
        'id_tag': machine,
        'business': machine.location_name,
        'technician': 'Anthony Ackerman',
        'date': today,
    }
    invList = {}
    i = 1
    for item in item_list:
        invList['item_name_' + str(i)] = item
        i += 1
#ENDING HERE------------------------------------
    #new = apps.get_model('monthly_bills', 'vmax576_form').objects.all()
    invForm = inventory_sheets_form(initial=initial_data)
        
    if request.method == 'POST':
        gatheredData = {
            'lane1': {
                'item_name': request.POST['item_name_1'],
                'stock': request.POST['stock_1'],
                'removed': request.POST['removed_1'],
                'sold': request.POST['sold_1'],
                'added': request.POST['added_1'],
                'total': int(request.POST['stock_1']) - handleNumberIntEmpty(request.POST['removed_1']) + handleNumberIntEmpty(request.POST['added_1']),
                'notes': request.POST['notes_1'],
            },
            'lane2': {
                'item_name': request.POST['item_name_2'],
                'stock': request.POST['stock_2'],
                'removed': request.POST['removed_2'],
                'sold': request.POST['sold_2'],
                'added': request.POST['added_2'],
                'total': handleNumberIntEmpty(request.POST['stock_2']) - handleNumberIntEmpty(request.POST['removed_2']) + handleNumberIntEmpty(request.POST['added_2']),
                'notes': request.POST['notes_2'],
            },
            'lane3': {
                'item_name': request.POST['item_name_3'],
                'stock': request.POST['stock_3'],
                'removed': request.POST['removed_3'],
                'sold': request.POST['sold_3'],
                'added': request.POST['added_3'],
                'total': handleNumberIntEmpty(request.POST['stock_3']) - handleNumberIntEmpty(request.POST['removed_3']) + handleNumberIntEmpty(request.POST['added_3']),
                'notes': request.POST['notes_3'],
            },
            'lane4': {
                'item_name': request.POST['item_name_4'],
                'stock': request.POST['stock_4'],
                'removed': request.POST['removed_4'],
                'sold': request.POST['sold_4'],
                'added': request.POST['added_4'],
                'total': handleNumberIntEmpty(request.POST['stock_4']) - handleNumberIntEmpty(request.POST['removed_4']) + handleNumberIntEmpty(request.POST['added_4']),
                'notes': request.POST['notes_4'],
            },
            'lane5': {
                'item_name': request.POST['item_name_5'],
                'stock': request.POST['stock_5'],
                'removed': request.POST['removed_5'],
                'sold': request.POST['sold_5'],
                'added': request.POST['added_5'],
                'total': handleNumberIntEmpty(request.POST['stock_5']) - handleNumberIntEmpty(request.POST['removed_5']) + handleNumberIntEmpty(request.POST['added_5']),
                'notes': request.POST['notes_5'],
            },
            'lane6': {
                'item_name': request.POST['item_name_6'],
                'stock': request.POST['stock_6'],
                'removed': request.POST['removed_6'],
                'sold': request.POST['sold_6'],
                'added': request.POST['added_6'],
                'total': handleNumberIntEmpty(request.POST['stock_6']) - handleNumberIntEmpty(request.POST['removed_6']) + handleNumberIntEmpty(request.POST['added_6']),
                'notes': request.POST['notes_6'],
            },
            'lane7': {
                'item_name': request.POST['item_name_7'],
                'stock': request.POST['stock_7'],
                'removed': request.POST['removed_7'],
                'sold': request.POST['sold_7'],
                'added': request.POST['added_7'],
                'total': handleNumberIntEmpty(request.POST['stock_7']) - handleNumberIntEmpty(request.POST['removed_7']) + handleNumberIntEmpty(request.POST['added_7']),
                'notes': request.POST['notes_7'],
            },
            'lane8': {
                'item_name': request.POST['item_name_8'],
                'stock': request.POST['stock_8'],
                'removed': request.POST['removed_8'],
                'sold': request.POST['sold_8'],
                'added': request.POST['added_8'],
                'total': handleNumberIntEmpty(request.POST['stock_8']) - handleNumberIntEmpty(request.POST['removed_8']) + handleNumberIntEmpty(request.POST['added_8']),
                'notes': request.POST['notes_8'],
            }
        }
        #gatheredJSON = json.dumps(gatheredData)
        copyData = request.POST.copy()
        for x in range(8):
            laneLabel1 = 'lane_'+str(x+1)
            laneLabel2 = 'lane'+str(x+1)
            copyData[laneLabel1] = gatheredData[laneLabel2]
        print(copyData)
        A = vmax576_form(copyData)
        if A.is_valid():
            A.save()
        # data = inventory_sheets_form(copyData)
        # print(copyData)
        # if data.is_valid():
        #     data.save()
        # parseCollect = float(request.POST['collected'])
        # if parseCollect > 0:
        #     copyData2 = request.POST.copy()
        #     copyData2['category'] = 'Income'
        #     copyData2['transaction'] = id_tag + ' Revenue Collected'
        #     copyData2['deposit'] = parseCollect
        #     form = vending_finance_form(copyData2)
        #     if form.is_valid():
        #         form.save()
        return redirect('vmax576_is', type, id_tag)
            
    return render (request,'inventory_sheets/machine_blocks/VMAX576_block.html',{
        'invForm': invForm, 
        'type': type, 
        'id_tag': id_tag, 
        'itemsStocked': itemsStocked, 
        'item_list': item_list,
        'includeStr': includeStr,
        'invList': invList,
        'vmax576_oldData': vmax576_oldData
    })
    
@lock
def RS900_is(request, type, id_tag):
    today = datetime.date.today()
    machine = fleet_model.objects.all().filter(id_tag__exact=id_tag)
    if len(machine) > 0:
        machine = machine[0]
    includeStr = machine.model + '_block.html'
    itemsStocked = machine_stock_model.objects.all().filter(id_tag__id_tag__exact=id_tag, discontinued=False).order_by('itemID')
    machineLayout = jsonSort(itemsStocked)
# STARTING HERE SPECIFICALLY FOR vmax576-------------
    item_list = []
    for x in itemsStocked:
        item_list.append(x.name)
        
    if len(item_list) != 29:
        diff = 29-len(item_list)
        for numb in range(diff):
            item_list.append('--none--')
        
    
    initial_data = {
        'id_tag': machine,
        'business': machine.location_name,
        'technician': 'Anthony Ackerman',
        'date': today,
    }
    invList = {}
    i = 1
    for item in item_list:
        invList['item_name_' + str(i)] = item
        i += 1
#ENDING HERE------------------------------------
    #new = apps.get_model('monthly_bills', 'vmax576_form').objects.all()
    invForm = inventory_sheets_form(initial=initial_data)
               
    if request.method == 'POST':
        gatheredData = {
            'A1': [
                {'item_name': request.POST['item_A1']},
                {'stock': request.POST['stock_A1']},
                {'removed': request.POST['removed_A1']},
                {'sold': request.POST['sold_A1']},
                {'added': request.POST['added_A1']},
                {'notes': request.POST['notes_A1']},
            ],
            'A2': [
                {'item_name': request.POST['item_A2']},
                {'stock': request.POST['stock_A2']},
                {'removed': request.POST['removed_A2']},
                {'sold': request.POST['sold_A2']},
                {'added': request.POST['added_A2']},
                {'notes': request.POST['notes_A2']},
            ],
            'A3': [
                {'item_name': request.POST['item_A3']},
                {'stock': request.POST['stock_A3']},
                {'removed': request.POST['removed_A3']},
                {'sold': request.POST['sold_A3']},
                {'added': request.POST['added_A3']},
                {'notes': request.POST['notes_A3']},
            ],
            'A4': [
                {'item_name': request.POST['item_A4']},
                {'stock': request.POST['stock_A4']},
                {'removed': request.POST['removed_A4']},
                {'sold': request.POST['sold_A4']},
                {'added': request.POST['added_A4']},
                {'notes': request.POST['notes_A4']},
            ],
            'A5': [
                {'item_name': request.POST['item_A5']},
                {'stock': request.POST['stock_A5']},
                {'removed': request.POST['removed_A5']},
                {'sold': request.POST['sold_A5']},
                {'added': request.POST['added_A5']},
                {'notes': request.POST['notes_A5']},
            ],
            'B1': [
                {'item_name': request.POST['item_B1']},
                {'stock': request.POST['stock_B1']},
                {'removed': request.POST['removed_B1']},
                {'sold': request.POST['sold_B1']},
                {'added': request.POST['added_B1']},
                {'notes': request.POST['notes_B1']},
            ],
            'B2': [
                {'item_name': request.POST['item_B2']},
                {'stock': request.POST['stock_B2']},
                {'removed': request.POST['removed_B2']},
                {'sold': request.POST['sold_B2']},
                {'added': request.POST['added_B2']},
                {'notes': request.POST['notes_B2']},
            ],
            'B3': [
                {'item_name': request.POST['item_B3']},
                {'stock': request.POST['stock_B3']},
                {'removed': request.POST['removed_B3']},
                {'sold': request.POST['sold_B3']},
                {'added': request.POST['added_B3']},
                {'notes': request.POST['notes_B3']},
            ],
            'B4': [
                {'item_name': request.POST['item_B4']},
                {'stock': request.POST['stock_B4']},
                {'removed': request.POST['removed_B4']},
                {'sold': request.POST['sold_B4']},
                {'added': request.POST['added_B4']},
                {'notes': request.POST['notes_B4']},
            ],
            'B5': [
                {'item_name': request.POST['item_B5']},
                {'stock': request.POST['stock_B5']},
                {'removed': request.POST['removed_B5']},
                {'sold': request.POST['sold_B5']},
                {'added': request.POST['added_B5']},
                {'notes': request.POST['notes_B5']},
            ],
            'B6': [
                {'item_name': request.POST['item_B6']},
                {'stock': request.POST['stock_B6']},
                {'removed': request.POST['removed_B6']},
                {'sold': request.POST['sold_B6']},
                {'added': request.POST['added_B6']},
                {'notes': request.POST['notes_B6']},
            ],
            'C1': [
                {'item_name': request.POST['item_C1']},
                {'stock': request.POST['stock_C1']},
                {'removed': request.POST['removed_C1']},
                {'sold': request.POST['sold_C1']},
                {'added': request.POST['added_C1']},
                {'notes': request.POST['notes_C1']},
            ],
            'C2': [
                {'item_name': request.POST['item_C2']},
                {'stock': request.POST['stock_C2']},
                {'removed': request.POST['removed_C2']},
                {'sold': request.POST['sold_C2']},
                {'added': request.POST['added_C2']},
                {'notes': request.POST['notes_C2']},
            ],
            'C3': [
                {'item_name': request.POST['item_C3']},
                {'stock': request.POST['stock_C3']},
                {'removed': request.POST['removed_C3']},
                {'sold': request.POST['sold_C3']},
                {'added': request.POST['added_C3']},
                {'notes': request.POST['notes_C3']},
            ],
            'C4': [
                {'item_name': request.POST['item_C4']},
                {'stock': request.POST['stock_C4']},
                {'removed': request.POST['removed_C4']},
                {'sold': request.POST['sold_C4']},
                {'added': request.POST['added_C4']},
                {'notes': request.POST['notes_C4']},
            ],
            'C5': [
                {'item_name': request.POST['item_C5']},
                {'stock': request.POST['stock_C5']},
                {'removed': request.POST['removed_C5']},
                {'sold': request.POST['sold_C5']},
                {'added': request.POST['added_C5']},
                {'notes': request.POST['notes_C5']},
            ],
            'C6': [
                {'item_name': request.POST['item_C6']},
                {'stock': request.POST['stock_C6']},
                {'removed': request.POST['removed_C6']},
                {'sold': request.POST['sold_C6']},
                {'added': request.POST['added_C6']},
                {'notes': request.POST['notes_C6']},
            ],
            'C7': [
                {'item_name': request.POST['item_C7']},
                {'stock': request.POST['stock_C7']},
                {'removed': request.POST['removed_C7']},
                {'sold': request.POST['sold_C7']},
                {'added': request.POST['added_C7']},
                {'notes': request.POST['notes_C7']},
            ],
            'C8': [
                {'item_name': request.POST['item_C8']},
                {'stock': request.POST['stock_C8']},
                {'removed': request.POST['removed_C8']},
                {'sold': request.POST['sold_C8']},
                {'added': request.POST['added_C8']},
                {'notes': request.POST['notes_C8']},
            ],
            'C9': [
                {'item_name': request.POST['item_C9']},
                {'stock': request.POST['stock_C9']},
                {'removed': request.POST['removed_C9']},
                {'sold': request.POST['sold_C9']},
                {'added': request.POST['added_C9']},
                {'notes': request.POST['notes_C9']},
            ],
            'C10': [
                {'item_name': request.POST['item_C10']},
                {'stock': request.POST['stock_C10']},
                {'removed': request.POST['removed_C10']},
                {'sold': request.POST['sold_C10']},
                {'added': request.POST['added_C10']},
                {'notes': request.POST['notes_C10']},
            ],
            'D1': [
                {'item_name': request.POST['item_D1']},
                {'stock': request.POST['stock_D1']},
                {'removed': request.POST['removed_D1']},
                {'sold': request.POST['sold_D1']},
                {'added': request.POST['added_D1']},
                {'notes': request.POST['notes_D1']},
            ],
            'D2': [
                {'item_name': request.POST['item_D2']},
                {'stock': request.POST['stock_D2']},
                {'removed': request.POST['removed_D2']},
                {'sold': request.POST['sold_D2']},
                {'added': request.POST['added_D2']},
                {'notes': request.POST['notes_D2']},
            ],
            'D3': [
                {'item_name': request.POST['item_D3']},
                {'stock': request.POST['stock_D3']},
                {'removed': request.POST['removed_D3']},
                {'sold': request.POST['sold_D3']},
                {'added': request.POST['added_D3']},
                {'notes': request.POST['notes_D3']},
            ],
            'D4': [
                {'item_name': request.POST['item_D4']},
                {'stock': request.POST['stock_D4']},
                {'removed': request.POST['removed_D4']},
                {'sold': request.POST['sold_D4']},
                {'added': request.POST['added_D4']},
                {'notes': request.POST['notes_D4']},
            ],
            'D5': [
                {'item_name': request.POST['item_D5']},
                {'stock': request.POST['stock_D5']},
                {'removed': request.POST['removed_D5']},
                {'sold': request.POST['sold_D5']},
                {'added': request.POST['added_D5']},
                {'notes': request.POST['notes_D5']},
            ],
            'D6': [
                {'item_name': request.POST['item_D6']},
                {'stock': request.POST['stock_D6']},
                {'removed': request.POST['removed_D6']},
                {'sold': request.POST['sold_D6']},
                {'added': request.POST['added_D6']},
                {'notes': request.POST['notes_D6']},
            ],
            'D7': [
                {'item_name': request.POST['item_D7']},
                {'stock': request.POST['stock_D7']},
                {'removed': request.POST['removed_D7']},
                {'sold': request.POST['sold_D7']},
                {'added': request.POST['added_D7']},
                {'notes': request.POST['notes_D7']},
            ],
            'D8': [
                {'item_name': request.POST['item_D8']},
                {'stock': request.POST['stock_D8']},
                {'removed': request.POST['removed_D8']},
                {'sold': request.POST['sold_D8']},
                {'added': request.POST['added_D8']},
                {'notes': request.POST['notes_D8']},
            ],
        }
        gatheredJSON = json.dumps(gatheredData)
        copyData = request.POST.copy()
        copyData['data'] = gatheredJSON
        data = inventory_sheets_form(copyData)

        for old in itemsStocked:
            for new in gatheredData:
                itemName = gatheredData[new][0]['item_name']
                itemStock = gatheredData[new][1]['stock']
                if old.name == itemName:
                    old.in_stock = itemStock
                    print('update')
        
        if data.is_valid():
            data.save()
            print('save')
            # pull_data = vmax576_model.objects.all().filter(date=request.POST['date'])[0]
            # for k in pull_data:
            #     if k ==
            # for product in itemsStocked:
            #     for stock in request.POST:
            #         if product.name == stock:
            #             product.in_stock = product.in_stock -
            ##return redirect('stock', type, id_tag)
        # for x in stockModel:
        #     # if x.title == y.title:
        #     #     x.amount = new amount
    
    return render (request,'inventory_sheets/machine_blocks/RS900_block.html',{
        'invForm': invForm, 
        'type': type, 
        'id_tag': id_tag, 
        'itemsStocked': itemsStocked, 
        'item_list': item_list,
        'includeStr': includeStr,
        'invList': invList,
        'machineLayout': machineLayout,
    })

@lock
def vmax576_rd(request, type, id_tag):
    today = datetime.datetime.now().date()
    products = productName(id_tag)
    vmax576_data = vmax576_model.objects.all()
    if vmax576_data.exists():
        firstEntryDate = vmax576_data[0].date
        presentEntryDate = vmax576_data.order_by('-date')[0].date
        firstMonth = firstEntryDate.month
        firstYear = firstEntryDate.year
        firstYear2 = firstEntryDate.year
        presentMonth = presentEntryDate.month
        presentYear = presentEntryDate.year
        monthlyTotals = {}
        annualTotals = {}
        print('Initiallizing Yearly...')
        for year1 in range((presentYear-firstYear)+1):
            print('Now checking year '+ str(firstYear))
            lane_1_build_annual = 0
            lane_2_build_annual = 0
            lane_3_build_annual = 0
            lane_4_build_annual = 0
            lane_5_build_annual = 0
            lane_6_build_annual = 0
            lane_7_build_annual = 0
            lane_8_build_annual = 0
            for log_id1, log1 in enumerate(vmax576_data.order_by('-date')):
                if log1.date.year == firstYear:
                    if log1.lane_1:
                        if log1.lane_1['added'] and log1.lane_1['added'] != 0:
                            lane_1_build_annual += int(log1.lane_1['added'])
                    if log1.lane_2:
                        if log1.lane_2['added'] and log1.lane_2['added'] != 0:
                            lane_2_build_annual += int(log1.lane_2['added'])
                    if log1.lane_3:
                        if log1.lane_3['added'] and log1.lane_3['added'] != 0:
                            lane_3_build_annual += int(log1.lane_3['added'])
                    if log1.lane_4:
                        if log1.lane_4['added'] and log1.lane_4['added'] != 0:
                            lane_4_build_annual += int(log1.lane_4['added'])
                    if log1.lane_5:
                        if log1.lane_5['added'] and log1.lane_5['added'] != 0:
                            lane_5_build_annual += int(log1.lane_5['added'])
                    if log1.lane_6:
                        if log1.lane_6['added'] and log1.lane_6['added'] != 0:
                            lane_6_build_annual += int(log1.lane_6['added'])
                    if log1.lane_7:
                        if log1.lane_7['added'] and log1.lane_7['added'] != 0:
                            lane_7_build_annual += int(log1.lane_7['added'])
                    if log1.lane_8:
                        if log1.lane_8['added'] and log1.lane_8['added'] != 0:
                            lane_8_build_annual += int(log1.lane_8['added'])
            yearTotalList = (lane_1_build_annual, lane_2_build_annual, lane_3_build_annual, lane_4_build_annual, lane_5_build_annual, lane_6_build_annual, lane_7_build_annual, lane_8_build_annual)
            annualTotals[str(firstYear)] = yearTotalList
            firstYear += 1
        print('Ending the Yearly Process...')
            
        print('Initiallizing Monthly...')
        for year2 in range((presentYear-firstYear2)+1):
            print('Now checking year '+ str(firstYear2))
            monthlyCollector = {}
            for month in range(12):
                month = month + 1
                lane_1_build_month = 0
                lane_2_build_month = 0
                lane_3_build_month = 0
                lane_4_build_month = 0
                lane_5_build_month = 0
                lane_6_build_month = 0
                lane_7_build_month = 0
                lane_8_build_month = 0
                print('Now checking '+ calendar.month_name[month] + ' in the year ' + str(firstYear2))
                for log_id2, log2 in enumerate(vmax576_data.order_by('-date')):
                    if log2.date.year == firstYear2:
                        if log2.date.month == month:
                            if log2.lane_1:
                                if log2.lane_1['added'] and log2.lane_1['added'] != 0:
                                    lane_1_build_month += int(log2.lane_1['added'])
                            if log2.lane_2:
                                if log2.lane_2['added'] and log2.lane_2['added'] != 0:
                                    lane_2_build_month += int(log2.lane_2['added'])
                            if log2.lane_3:
                                if log2.lane_3['added'] and log2.lane_3['added'] != 0:
                                    lane_3_build_month += int(log2.lane_3['added'])
                            if log2.lane_4:
                                if log2.lane_4['added'] and log2.lane_4['added'] != 0:
                                    lane_4_build_month += int(log2.lane_4['added'])
                            if log2.lane_5:
                                if log2.lane_5['added'] and log2.lane_5['added'] != 0:
                                    lane_5_build_month += int(log2.lane_5['added'])
                            if log2.lane_6:
                                if log2.lane_6['added'] and log2.lane_6['added'] != 0:
                                    lane_6_build_month += int(log2.lane_6['added'])
                            if log2.lane_7:
                                if log2.lane_7['added'] and log2.lane_7['added'] != 0:
                                    lane_7_build_month += int(log2.lane_7['added'])
                            if log2.lane_8:
                                if log2.lane_8['added'] and log2.lane_8['added'] != 0:
                                    lane_8_build_month += int(log2.lane_8['added'])
                monthTotalList = (lane_1_build_month, lane_2_build_month, lane_3_build_month, lane_4_build_month, lane_5_build_month, lane_6_build_month, lane_7_build_month, lane_8_build_month)
                print(calendar.month_name[month], monthTotalList)
                monthlyCollector[calendar.month_name[month]] = monthTotalList
            monthlyTotals[str(firstYear2)] = monthlyCollector
            firstYear2 += 1
        
        print(annualTotals)
        print(monthlyTotals)
    return render(request, 'restock_data.html', {
        'type': type,
        'id_tag': id_tag,
        'products': products,
        'annualTotals': annualTotals,
        'monthlyTotals': monthlyTotals
    })

@lock
def universal_is(request, type, id_tag, buildID):
    today = datetime.date.today()
    machine = fleet_model.objects.get(id_tag__exact=id_tag)
    machineList = machine_build_model.objects.filter(machineChoice__id_tag=id_tag).order_by('-date')
    if buildID != "default":
        machineData = machine_build_model.objects.get(id=buildID)
    else:
        machineData = machineList[0]
    initial_data = {
        'id_tag': machine,
        'business': machine.location_name,
        'technician': request.user.get_full_name(),
        'date': today,
    }
    pastInventory = inventory_sheets_model.objects.filter(id_tag=machine).order_by('-date')
    if pastInventory.exists():
        pastInventory = sorted(pastInventory[0].data.items())
    else:
        pastInventory = False
    allItems = item_data_model.objects.all()
    organizedBuildData = sorted(machineData.slot_dictionary.items())
    print(organizedBuildData)
    rebuildDataStart = []
    for buildLane in organizedBuildData:
        for sItems in allItems:
            if buildLane[1]['itemID'] == sItems.itemID:
                rebuildDataStart.append((buildLane[0], sItems.name))
        if buildLane[1]['itemID'] == 'empty':
            rebuildDataStart.append((buildLane[0], 'EMPTY'))
    if pastInventory:
        newReBuild = []
        for rebu in rebuildDataStart:
            empty = True
            for pastInven in pastInventory:
                if rebu[0] == pastInven[0]:
                    print(pastInven[1])
                    newReBuild.append((rebu[0], rebu[1], pastInven[1]))
                    empty = False
            if empty == True:
                newList = {'item_name': rebu[1], 'stock': '0', 'removed': '0', 'sold': '0', 'added': '0', 'notes': '-', 'new_dates': ''}
                newReBuild.append((rebu[0], rebu[1], newList))
        rebuildData = newReBuild
    else:
        rebuildData = rebuildDataStart
    invForm = inventory_sheets_form(initial=initial_data)
               
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        if 'machineBuild' in data.keys():
            return redirect('inventorySheet', type, id_tag, data['machineBuild'])
        gatheredData = {}
        for buildLane in rebuildData:
            if 'new_dates_'+str(buildLane[0]) in data.keys():
                gatheredData[buildLane[0]] = {
                    'item_name': data['item_'+str(buildLane[0])],
                    'stock': data['stock_'+str(buildLane[0])],
                    'removed': str(-int(data['removed_'+str(buildLane[0])])),
                    'sold': data['sold_'+str(buildLane[0])],
                    'added': data['added_'+str(buildLane[0])],
                    'notes': data['notes_'+str(buildLane[0])],
                    'new_dates': data['new_dates_'+str(buildLane[0])]
                }
            else:
                gatheredData[buildLane[0]] = {
                    'item_name': data['item_'+str(buildLane[0])],
                    'stock': data['stock_'+str(buildLane[0])],
                    'removed': str(-int(data['removed_'+str(buildLane[0])])),
                    'sold': data['sold_'+str(buildLane[0])],
                    'added': data['added_'+str(buildLane[0])],
                    'notes': data['notes_'+str(buildLane[0])],
                    'new_dates': ""
                }
        gatheredJSON = json.loads(json.dumps(gatheredData))
        copyData = data.copy()
        copyData['data'] = gatheredJSON
        copyData['machineBuild'] = machineData
        data = inventory_sheets_form(copyData)

        if data.is_valid():
            A = data.save()
            jsonData = A.data

            for key, itemData in jsonData.items():
                itemName = itemData['item_name']
                itemID = item_data_model.objects.get(name=itemName).id
                at_home_stock_for_item = home_inventory_model.objects.get(item__id=itemID)
                change = -int(itemData['added'])
                at_home_stock_for_item.update_stock(change, "Added to machine")

            print('save')
            return redirect('machineDash', type, id_tag)
    
    return render (request,'inventory_sheets/universal_is.html',{
        'invForm': invForm, 
        'type': type, 
        'id_tag': id_tag, 
        'organizedBuildData': rebuildData,
        'pastInventory': pastInventory,
        'goBack': 'options',
        'machineList': machineList,
        'rebuildDataStart': rebuildDataStart
    })
 
@lock
def view_is(request, type, id_tag, date):
    goBack = 'options'
    machine = fleet_model.objects.get(id_tag__exact=id_tag)
    currentInventory = inventory_sheets_model.objects.get(id_tag=machine, date=date)
    machineData = machine_build_model.objects.get(machineChoice__id_tag=id_tag, id=currentInventory.machineBuild.id)
    currentInventoryData = currentInventory
    currentInventory = sorted(currentInventory.data.items())

    allItems = item_data_model.objects.all()
    organizedBuildData = sorted(machineData.slot_dictionary.items())
    rebuildData = []
    for buildLane in organizedBuildData:
        for sItems in allItems:
            if buildLane[1]['itemID'] == sItems.itemID:
                rebuildData.append((buildLane[0], sItems.name))
        if buildLane[1]['itemID'] == 'empty':
            rebuildData.append((buildLane[0], 'EMPTY'))
    if currentInventory:
        newReBuild = []
        for rebu in rebuildData:
            for currentInven in currentInventory:
                if rebu[0] == currentInven[0]:
                    newReBuild.append((rebu[0], rebu[1], currentInven[1]))
        rebuildData = newReBuild
    print(rebuildData)
    return render (request,'inventory_sheets/view_is.html',{
        'goBack': goBack,
        'type': type, 
        'id_tag': id_tag, 
        'organizedBuildData': rebuildData,
        'currentInventory': currentInventory,
        'currentInventoryData': currentInventoryData
    })

@lock
def canta_payments(request, type, id_tag):
    goBack = 'options'
    machine = fleet_model.objects.get(id_tag__exact=id_tag)
    initial_data = {
        "machineChoice": machine
    }
    form = canta_payments_form(initial=initial_data)
    
    if request.method == 'POST':
        data = request.POST
        dataForm = canta_payments_form(data)
        print(dataForm.errors)
        if dataForm.is_valid():
            dataForm.save()
            print('save')
            return redirect('machineDash', type, id_tag)
    
    return render (request,'canta_payments.html',{
        'goBack': goBack,
        'type': type, 
        'id_tag': id_tag,
        'form': form
    })
