from django.shortcuts import render, redirect
from ..models import fleet_model, item_data_model, machine_build_model
from ..forms import fleet_form, machine_build_form
from django.contrib.auth.decorators import login_required
import json
import datetime
lock = login_required(login_url='login')

@lock
def fleet(request):
    fleet = fleet_model.objects.all()
    nonActive = True
    availability = False
    
    modelParseDict = {}
    for x in fleet:
        if x.active:
            nonActive=False
        else:
            availability = True
        
        modelParseDict[x.model] = x.model.replace('-', '_')

    return render (request,'fleet.html',{
        'fleet': fleet, 
        'nonActive': nonActive, 
        'availability': availability,
        'modelParseDict': modelParseDict
    })

@lock
def add_fleet(request, selector):
    if selector != 'add':
        selMachine = fleet_model.objects.all().filter(id_tag__exact=selector)[0]
        initial_data = {
            'id_tag': selMachine.id_tag,
            'machine_type': selMachine.machine_type,
            'model': selMachine.model,
            'key_id': selMachine.key_id,
            'serial_num': selMachine.serial_num,
            'buy_price': selMachine.buy_price,
            'date_bought': selMachine.date_bought,
            'location_name': selMachine.location_name,
            'address': selMachine.address,
            'contact_name': selMachine.contact_name,
            'phone': selMachine.phone,
            'in_service': selMachine.in_service,
            'last_service': selMachine.last_service,
            'next_servicing': selMachine.next_servicing,
            'notes': selMachine.notes,
            'active': selMachine.active,
        }
        data = fleet_form(initial=initial_data)
    else:
        data = fleet_form 

    if request.method == 'POST':
        if selector != 'add':
            form = fleet_form(request.POST, instance=selMachine)
        else:
            form = fleet_form(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect ('fleet')
    
    
    return render (request,'add_fleet.html',{
        'fleet': data, 'selector': selector
    })
    
@lock
def machine_build_view(request, machineID):
    formData = False
    snackData = item_data_model.objects.all()
    machineData = fleet_model.objects.get(id_tag=machineID)
    buildQuery = machine_build_model.objects.filter(machineChoice__id_tag=machineID).order_by('-date')
    today = datetime.datetime.today().date()
    if buildQuery.exists():
        form = buildQuery[0]
        formData = True
        
        dataDict = {}
        snackLanes = 0
        drinkLanes = 0
        drinkLaneData = []
        snackLaneData = []
        for lane in form.slot_dictionary.items():
            if lane[1]['size'] != 'regular':
                snackLanes += 1
                snackLaneData.append(lane)
            else:
                drinkLanes += 1
                drinkLaneData.append(lane)
            
        dataDict['snackLanes'] = snackLanes
        dataDict['drinkLanes'] = drinkLanes
        dataDict['drinkLaneData'] = drinkLaneData
        dataDict['snackLaneData'] = snackLaneData
        print(dataDict['drinkLaneData'])
    
    if request.method == 'POST':
        data = request.POST
        if not formData:
            snackLanes = int(data['snack_lane_qty'])
            drinkLanes = int(data['drink_lane_qty'])
        laneDict = {}
        for lane in range(1, snackLanes+1):
            laneID = "S"+str(lane)
            buildlane = {'itemID':data['itemID_'+laneID],'slots':data['slots_'+laneID], 'size':data['size_'+laneID], 'cost':data['cost_'+laneID]}
            laneDict[data['selectID_'+laneID]] = buildlane
        for lane in range(1, drinkLanes+1):
            laneID = "D"+str(lane)
            buildlane = {'itemID':data['itemID_'+laneID],'slots':data['slots_'+laneID], 'size':data['size_'+laneID], 'cost':data['cost_'+laneID]}
            laneDict[data['selectID_'+laneID]] = buildlane
        print(laneDict)         
        dataCopy = request.POST.copy()
        dataCopy['machineChoice'] = machineData
        dataCopy['slot_dictionary'] = json.dumps(laneDict)
        dataForm = machine_build_form(dataCopy)
        print(dataForm.errors)
        if dataForm.is_valid():
            dataForm.save()
            return redirect('fleet')
    return render(request, 'machines/machine_builds.html', {
        'machineID': machineID,
        'snackData': snackData,
        'today': str(today),
        'form': form,
        'formData': formData,
        'dataDict': dataDict
    })
    # {% if formData %}{% else %}{% endif %}