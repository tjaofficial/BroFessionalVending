from .models import *
from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

# class add_bills_form(ModelForm):
#     class Meta:
#         model = bill_items_model
#         fields = ('__all__')
#         widgets = {
#             'category' : forms.Select(attrs={'style':'width: 150px;'}),
#             'est_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
#             'title' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
#             'budget_amt' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
#             'monthly_period' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
#         }
        
class add_bills_form(ModelForm):
    class Meta:
        model = bills_model
        fields = ('__all__')
        widgets = {
            'title' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'budget_amt' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'billing_period' : forms.Select(attrs={'style':'width:50px;'}),
            'charge_day_1' : forms.NumberInput(attrs={'type': 'number', 'style':'width: 140px;'}),
            'charge_day_2' : forms.NumberInput(attrs={'type': 'number', 'style':'width: 140px;'}),
            'category' : forms.Select(attrs={'style':'width: 150px;'}),
            'source' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'start_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'stop_date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
        }
        
class pay_log_form(ModelForm):
    class Meta:
        form = bill_items_model.objects.all()
        form2 = purchase_model.objects.all()
    
        A =[]
        for x in form:
            A.append((str(x.title),str(x.title)),)
        for y in form2:
            this = str(y.title),str(y.title)
            if this in A:
                continue
            else:
                A.append((str(y.title),str(y.title)),)
            
        bill_select = tuple(A)
        
        bill_select = sorted(A, key = lambda x: (x[1], x[0]))
        
        model = pay_log
        fields = ('__all__')
        widgets = {
            'bill' : forms.Select(choices=bill_select, attrs={'style':'width: 150px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'payment' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
        }
        
class income_log_form(ModelForm):
    class Meta:
        model = income_log
        fields = ('__all__')
        widgets = {
            'title' : forms.Select(attrs={'style':'width: 150px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'amount' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
            'describe' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
        }
class add_purchase_form(ModelForm):
    class Meta:
        model = purchase_model
        fields = ('__all__')
        widgets = {
            'category' : forms.Select(attrs={'style':'width: 150px;'}),
            'date' : forms.DateInput(attrs={'type':'date', 'style':'width: 140px;'}),
            'title' : forms.TextInput(attrs={'type':'text', 'style':'width: 150px; text-align: center;'}),
            'amount' : forms.NumberInput(attrs={'type': 'number', 'style':'width:50px;'}),
        }
        
class fleet_form(ModelForm):
    active = forms.BooleanField(required=False)
    class Meta:
        model = fleet_model
        fields = ('__all__')
        widgets = {
            'id_tag' : forms.TextInput(attrs={'type':'text',}),
            'machine_type' : forms.Select(attrs={}),
            'model' : forms.TextInput(attrs={'type':'text',}),
            'key_id' : forms.TextInput(attrs={'type':'text',}),
            'serial_num' : forms.TextInput(attrs={'type':'text',}),
            'buy_price' : forms.NumberInput(attrs={'type':'number',}),
            'date_bought' : forms.DateInput(attrs={'type':'date'}),
            'location_name' : forms.TextInput(attrs={'type':'text',}),
            'address' : forms.TextInput(attrs={}),
            'contact_name' : forms.TextInput(attrs={'type':'text',}),
            'phone' : forms.TextInput(attrs={}),
            'in_service' : forms.DateInput(attrs={'type':'date'}),
            'last_service' : forms.DateInput(attrs={'type':'date'}),
            'next_servicing' : forms.DateInput(attrs={'type':'date'}),
            'notes' : forms.Textarea(attrs={'type':'textbox', 'style':''}),
            'active' : forms.BooleanField(),
        }
        
class machine_stock_form(ModelForm):
    cost_per_unit = forms.FloatField(required=False)
    sell_price = forms.FloatField(required=False)
    discontinued = forms.BooleanField(required=False)
    class Meta:
        model = machine_stock_model
        fields = ('__all__')
        #exclude = ('id_tag',)
        widgets = {
            'name' : forms.TextInput(attrs={'type':'text'}),
            'size' : forms.TextInput(attrs={'type':'text'}),
            'cost_per_unit' : forms.FloatField(),
            'sell_price' : forms.FloatField(),
            'vendor' : forms.TextInput(attrs={'type':'text'}),
            'qty_per_unit' : forms.NumberInput(attrs={'type':'number'}),
            'in_stock' : forms.NumberInput(attrs={'type':'number'}),
            'discontinued' : forms.BooleanField(),
        }
        
class vmax576_form(ModelForm):
    collected = forms.FloatField(required=False)
    class Meta:
        model = vmax576_model
        fields = ('__all__')
        widgets = {
            'business' : forms.TextInput(attrs={'type':'text'}),
            'date' : forms.DateInput(attrs={'type':'date'}),
            'time_start' : forms.TimeInput(attrs={'type':'time'}),
            'time_end' : forms.TimeInput(attrs={'type':'time'}),
            'technician' : forms.TextInput(attrs={'type':'text'}),
            'condition' : forms.Select(attrs={}),
            'collected' : forms.FloatField(),
            
            'item_name_1' : forms.TextInput(attrs={'style': 'width: 154px;'}),
            'lane_1' : forms.NumberInput(attrs={'type':'number', 'style': 'width:44px;'}),

            'item_name_2' : forms.TextInput(attrs={'style': 'width: 154px;'}),
            'lane_2' : forms.NumberInput(attrs={'type':'number', 'style': 'width:44px;'}),

            'item_name_3' : forms.TextInput(attrs={'style': 'width: 154px;'}),
            'lane_3' : forms.NumberInput(attrs={'type':'number', 'style': 'width:44px;'}),

            'item_name_4' : forms.TextInput(attrs={'style': 'width: 154px;'}),
            'lane_4' : forms.NumberInput(attrs={'type':'number', 'style': 'width:44px;'}),

            'item_name_5' : forms.TextInput(attrs={'style': 'width: 154px;'}),
            'lane_5' : forms.NumberInput(attrs={'type':'number', 'style': 'width:44px;'}),

            'item_name_6' : forms.TextInput(attrs={'style': 'width: 154px;'}),
            'lane_6' : forms.NumberInput(attrs={'type':'number', 'style': 'width:44px;'}),

            'item_name_7' : forms.TextInput(attrs={'style': 'width: 154px;'}),
            'lane_7' : forms.NumberInput(attrs={'type':'number', 'style': 'width:44px;'}),

            'item_name_8' : forms.TextInput(attrs={'style': 'width: 154px;'}),
            'lane_8' : forms.NumberInput(attrs={'type':'number', 'style': 'width:44px;'}),
        }
        
class gas_log_form(ModelForm):
    actual_cost = forms.FloatField(required=False)
    class Meta:
        model = gas_log_model
        fields = ('__all__')
        widgets = {
            'name' : forms.TextInput(attrs={'type':'text'}),
            'date' : forms.DateInput(attrs={'type':'date'}),
            'actual_cost' : forms.FloatField(),
            'description' : forms.TextInput(attrs={'type':'text'}),
        }
        
class mileage_log_form(ModelForm):
    mileage = forms.FloatField(required=False)
    class Meta:
        model = mileage_log_model
        fields = ('__all__')
        widgets = {
            'name' : forms.TextInput(attrs={'type':'text'}),
            'date' : forms.DateInput(attrs={'type':'date'}),
            'mileage' : forms.FloatField(),
            'description' : forms.TextInput(attrs={'type':'text'}),
        }
        
class inventory_sheets_form(ModelForm):
    collected = forms.FloatField(required=False)
    class Meta:
        model = inventory_sheets_model
        fields = ('__all__')
        widgets = {
            'business' : forms.TextInput(attrs={'type':'text'}),
            'date' : forms.DateInput(attrs={'type':'date'}),
            'time_start' : forms.TimeInput(attrs={'type':'time'}),
            'time_end' : forms.TimeInput(attrs={'type':'time'}),
            'technician' : forms.TextInput(attrs={'type':'text'}),
            'condition' : forms.Select(attrs={}),
            'collected' : forms.FloatField(),
            
            'data' : forms.TextInput(attrs={'style': 'width: 154px;'}),
        }
        
class vending_finance_form(ModelForm):
    withdrawal = forms.FloatField(required=False)
    deposit = forms.FloatField(required=False)
    class Meta:
        model = vending_finance
        fields = ('__all__')
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'}),
            'transaction' : forms.TextInput(attrs={'type':'text'}),
            'withdrawal' : forms.FloatField(),
            'deposit' : forms.FloatField(),
            'category' : forms.Select(attrs={}),
        }
        
class cantaLogs_form(ModelForm):
    class Meta:
        model = cantaLogs_model
        fields = ('__all__')
        widgets = {
            'id_tag' : forms.TextInput(attrs={}),
            'date' : forms.DateInput(attrs={'type':'date'}),
            'prev_count' : forms.TextInput(attrs={}),
            'adding' : forms.TextInput(attrs={}),
            'sold' : forms.TextInput(attrs={}),
        }