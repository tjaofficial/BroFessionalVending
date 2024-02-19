from .models import machine_stock_model

def productName(id_tag):
    stockModel = machine_stock_model.objects.filter(id_tag__id_tag__exact=id_tag, discontinued=False).order_by('itemID')
    productsList = []
    for x in stockModel:
        productsList.append(x.name)
    return productsList