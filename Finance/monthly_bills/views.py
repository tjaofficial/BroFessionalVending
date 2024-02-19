# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
#from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
#from operator import itemgetter
import datetime
import calendar
from calendar import HTMLCalendar
from .models import *
from .forms import *
#from .utils import EventCalendar, Calendar
#from dateutil.relativedelta import relativedelta
#from django.apps import apps
#from django.core.exceptions import FieldDoesNotExist, FieldError
from django.contrib.auth.models import User, Group




def dashboard(request):
    
    
    
    
    return render (request,'dashboard.html',{
        
    })
    