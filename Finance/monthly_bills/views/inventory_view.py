from django.shortcuts import render, redirect
from ..models import cantaLogs_model, price_model, fleet_model, machine_stock_model, vmax576_model, inventory_sheets_model
from ..forms import cantaLogs_form, machine_stock_form, vmax576_form, inventory_sheets_form, vending_finance_form
from ..utils import productName
import datetime
from django.apps import apps
import json
import calendar

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
    
def machine_options(request, type, id_tag):
    dataAll = inventory_sheets_model.objects.filter(id_tag__id_tag__exact=id_tag).order_by('-date')
    machine = fleet_model.objects.filter(id_tag__exact=id_tag)
    stockModel = machine_stock_model.objects.filter(id_tag__id_tag__exact=id_tag, discontinued=False).order_by('itemID')
    priceModel = price_model.objects.filter(machine_id=id_tag)
    cantaLogs = cantaLogs_model.objects.filter(id_tag__id_tag__exact=id_tag).order_by('-date')
    showForm = False
    
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

    totalCollected = 0.00
    for log in inventoryLogs:
        totalCollected += float(log.collected)
        
    if cantaLogs.exists():
        initial_data = {
            'date': cantaLogs[0].date + datetime.timedelta(days=1)
        }
    else:
        initial_data = {}
        
    cantaForm = cantaLogs_form(initial=initial_data)
    def handleEmpty(input):
            if input:
                input = int(input)
            else:
                input = 0
            return input    
            
    def cantaMath(dictLabel):
        print(dictLabel)
        if cantaLogs.exists():
            selectedCantaLog = cantaLogs[0]
        else:
            return False
        countStart = json.loads(selectedCantaLog.prev_count)[dictLabel]
        if len(json.loads(selectedCantaLog.adding)) > 0:
            countAdd = handleEmpty(json.loads(selectedCantaLog.adding)[dictLabel])
        else:
            countAdd = 0
        if len(json.loads(selectedCantaLog.sold)) > 0:
            countSold = handleEmpty(json.loads(selectedCantaLog.sold)[dictLabel])
            print(countSold)
        else:
            countSold = 0
        print(countAdd)
        print(countSold)
        newTotal = countStart + countAdd - countSold
        return newTotal
    
    def cantaCount():
        newCount = []
        for x in range(8):
            print(x)
            newCount.append(cantaMath(str(x+1)))
        return newCount
        
    
    
    canta = cantaCount()
    print(cantaCount())
    products = productName(id_tag)
    
    machineLayout = jsonSort(stockModel)

    if len(priceModel) > 0:
        priceModel = priceModel[0]
        prices = json.loads(priceModel.price_JSON)
    else:
        prices = {}
    
    totalCollect = 0
    laneList = []
    for money in dataAll:
        #print('Grabbing inventroy Sheet...')
        #print(money)
        inven = json.loads(money.data)
        for lane in inven:
            laneList.append((money, inven[lane]['item_name'],inven[lane]['stock'], inven[lane]['removed'], inven[lane]['sold'], inven[lane]['added'], inven[lane]['notes']))
        totalCollect += money.collected
    totalCollect = format(totalCollect, '.2f')
    
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        addCount = False
        soldCount = False
        for x in range(8):
            lineAdd = data['addP'+str(x+1)]
            if lineAdd and int(lineAdd) > 0:
                addCount = True
        for x in range(8):
            print(x)
            lineSold = data['soldP'+str(x+1)]
            if lineSold and int(lineSold) > 0:
                soldCount = True
                
        prevCount = {
                "1": canta[0],
                "2": canta[1],
                "3": canta[2],
                "4": canta[3],
                "5": canta[4],
                "6": canta[5],
                "7": canta[6],
                "8": canta[7]
                }
        if addCount:
            added = {
                "1": handleEmpty(data['addP1']),
                "2": handleEmpty(data['addP2']),
                "3": handleEmpty(data['addP3']),
                "4": handleEmpty(data['addP4']),
                "5": handleEmpty(data['addP5']),
                "6": handleEmpty(data['addP6']),
                "7": handleEmpty(data['addP7']),
                "8": handleEmpty(data['addP8'])
                }
        else:
            added = {}
        if soldCount:
            sold = {
                "1": handleEmpty(data['soldP1']),
                "2": handleEmpty(data['soldP2']),
                "3": handleEmpty(data['soldP3']),
                "4": handleEmpty(data['soldP4']),
                "5": handleEmpty(data['soldP5']),
                "6": handleEmpty(data['soldP6']),
                "7": handleEmpty(data['soldP7']),
                "8": handleEmpty(data['soldP8'])
                }
        else:
            sold = {}

        added = json.dumps(added)
        sold = json.dumps(sold)
        prevCount = json.dumps(prevCount)
        
        print(added)
        copyData = request.POST.copy()
        copyData['adding'] = added
        copyData['sold'] = sold
        copyData['id_tag'] = machine
        copyData['prev_count'] = prevCount
        print(cantaLogs_form(copyData).errors)
        if cantaLogs_form(copyData).is_valid():
            cantaLogs_form(copyData).save()
            print('IT HAS BEEN SAVED')
            return redirect('machineDash', type, id_tag)

    return render (request,'machine_options.html',{
        'inventoryLogs': inventoryLogs, 
        'cantaForm': cantaForm, 
        'products': products, 
        'canta': canta, 
        'prices': prices, 
        'machineLayout': machineLayout, 
        'type': type, 
        'id_tag': id_tag, 
        'data': laneList, 
        'totalCollect': totalCollect, 
        'machineURL': machineURL, 
        'machine': machine,
        'totalCollected': totalCollected,
        'showForm': showForm
    })   
    
def stock(request, type, id_tag):
    stock = machine_stock_model.objects.all().filter(id_tag__id_tag__exact=id_tag)
    
    return render (request,'machine_stock.html',{
        'type': type, 'id_tag': id_tag, 'stock': stock
    })
    
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
    
def GF12_3506_3506A_is(request, type, id_tag):
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
    
    return render (request,'inventory_sheets/machine_blocks/GF12-3506_block.html',{
        'invForm': invForm, 
        'type': type, 
        'id_tag': id_tag, 
        'itemsStocked': itemsStocked, 
        'item_list': item_list,
        'includeStr': includeStr,
        'invList': invList,
        'machineLayout': machineLayout,
    })
    