from django.shortcuts import render, redirect
from ..models import fleet_model
from ..forms import fleet_form

def fleet(request):
    fleet = fleet_model.objects.all()
    nonActive = True
    availability = False
    
    for x in fleet:
        if x.active:
            nonActive=False
        else:
            availability = True
        
    
    
    return render (request,'fleet.html',{
        'fleet': fleet, 'nonActive': nonActive, 'availability': availability
    })
    
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