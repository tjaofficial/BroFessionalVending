from django.shortcuts import render, redirect
from ..models import inventory_sheets_model
import json

def analytics_page(request, type, id_tag):
    invenSheets = inventory_sheets_model.objects.filter(id_tag__id_tag=id_tag).order_by('date')
    monthsList = []
    for sheet in invenSheets:
        lengthOfList = len(monthsList)
        date = sheet.date
        month = sheet.date.month
        year = sheet.date.year
        if lengthOfList > 0:
            if month != monthsList[lengthOfList-1][0]:
                monthsList.append([month, year])
            else:
                continue
        else:
            monthsList.append([month, year])
    print(monthsList)
    finalList = []
    for dateList in monthsList:
        monthlySheets = invenSheets.filter(date__month=dateList[0], date__year=dateList[1])
        totalSold = 0
        for monSheet in monthlySheets:
            for key, lane in json.loads(monSheet.data).items():
                print(lane[3]["sold"])
                break
            break
        break
            
    
    return render(request, 'analytics/analyticsDash.html', {
        'disable_links': True,
        'goBack': 'vendDash',
        'type': type, 
        'id_tag': id_tag,
        'xAxix': monthsList
    })