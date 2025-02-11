from .models import machine_stock_model, item_data_model, machine_build_model

def productName(id_tag):
    stockModel = machine_stock_model.objects.filter(id_tag__id_tag__exact=id_tag, discontinued=False).order_by('itemID')
    productsList = []
    for x in stockModel:
        productsList.append(x.name)
    return productsList

def getItemPriceByName(id_tag, item_name):
    itemQuery = item_data_model.objects.get()
    buildQuery = machine_build_model.objects.filter(machineChoice__id_tag=id_tag).order_by('-date')
    if buildQuery.exists():
        buildQuery = buildQuery[0]
        print(buildQuery.slot_dictionary)

def find_machines_with_item(itemID):
    # Total Sold Query adn Amount
    machines_with_item = []

    # Get all machine records
    machines = machine_build_model.objects.all()

    for machine in machines:
        try:
            # Get slot dictionary
            slot_dict = machine.slot_dictionary  # JSONField, already a dict

            for lane, details in slot_dict.items():
                if details.get("itemID") == itemID:
                    print(machine)
                    print(details.get("cost", 1.50))
                    machines_with_item.append({
                        "machine": str(machine.machineChoice),
                        "date": str(machine.date),
                        "lane": lane,  # Store the lane where the itemID was found
                        "cost": details.get("cost", 1.50)
                    })
        except Exception as e:
            print(f"Error processing machine {machine}: {e}")
    return machines_with_item