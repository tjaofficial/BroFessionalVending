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
    