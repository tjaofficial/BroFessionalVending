from django.shortcuts import render
from ..models import FAQ_model

def landing_page(request):
    
    return render (request,'landing/landing_main.html',{})

def FAQ_page(request):
    FAQData = FAQ_model.objects.all().order_by('-id')
    return render (request,'landing/FAQ.html',{
        'FAQData': FAQData
    })
    
def contact_page(request):
    
    return render (request,'landing/contact.html',{})