from django.shortcuts import render, redirect
from ..models import inventory_sheets_model
import json

def analytics_page(request, type, id_tag):
    invenSheets = inventory_sheets_model.objects.filter(id_tag__id_tag=id_tag).order_by('date')
    itemList = {}
    for sheet in invenSheets:
        itemDate = sheet.date
        sellData = json.loads(sheet.data)
        soldList = []
        for itemID, itemData in sellData.items():
            itemName = itemData[0]['item_name']
            itemSold = itemData[3]['sold']
            if itemSold == '':
                itemSold = 0
            else:
                itemSold = int(itemSold)
            if itemName in itemList.keys():
                itemList[itemName]['sold_list'].append(itemSold)
                itemList[itemName]['date_list'].append([itemDate.month, itemDate.day, itemDate.year])
            else:
                print('hell no')
                itemList[itemName] = {
                    'sold_list': [itemSold],
                    'date_list': [[itemDate.month, itemDate.day, itemDate.year]]
                }
            
            # soldList.append(itemSold)
            # itemList.append({'item_name': itemName, 'sold_list': itemSold, 'date_list': itemDate})
    print(itemList)
        
        
            # {
            #     'reeses': {
            #         'sold_list': [INCLUDE SOLD HERE],
            #         'date_list': [INCLUDE DATES HERE]
            #     }
            # }
        
        
        # date = sheet.date
        # month = sheet.date.month
        # year = sheet.date.year
        # if lengthOfList > 0:
        #     if month != monthsList[lengthOfList-1][0]:
        #         monthsList.append([month, year])
        #     else:
        #         continue
        # else:
        #     monthsList.append([month, year])
    
    
    # for sheet in invenSheets:
    #     lengthOfList = len(monthsList)
    #     date = sheet.date
    #     month = sheet.date.month
    #     year = sheet.date.year
    #     if lengthOfList > 0:
    #         if month != monthsList[lengthOfList-1][0]:
    #             monthsList.append([month, year])
    #         else:
    #             continue
    #     else:
    #         monthsList.append([month, year])
    # print(monthsList)
    # finalList = []
    # for dateList in monthsList:
    #     monthlySheets = invenSheets.filter(date__month=dateList[0], date__year=dateList[1])
    #     totalSold = 0
    #     for monSheet in monthlySheets:
    #         for key, lane in json.loads(monSheet.data).items():
    #             productSold = lane[3]["sold"]
    #             if productSold != '':
    #                 totalSold
    #             print(lane[3]["sold"])
    #             break
    #         break
    #     break
            
    
    return render(request, 'analytics/analyticsDash.html', {
        'disable_links': True,
        'goBack': 'vendDash',
        'type': type, 
        'id_tag': id_tag,
        'itemList': itemList,
    })