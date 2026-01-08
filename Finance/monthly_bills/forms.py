from .models import *
from django import forms #type: ignore
from django.forms import ModelForm, Textarea #type: ignore
from django.contrib.auth.forms import UserCreationForm #type: ignore
from django.contrib.auth.models import User #type: ignore
from .utils import find_machines_with_item
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
            'collected' : forms.NumberInput(attrs={'step':'0.01', 'required':True}),
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
        
class item_data_form(ModelForm):
    discontinued = forms.BooleanField(required=False)
    class Meta:
        model = item_data_model
        fields = ('__all__')
        widgets = {
            'itemID': forms.TextInput(attrs={'type':'text'}),
            'name' : forms.TextInput(attrs={'type':'text'}),
            'itemType': forms.Select(),
            'container_description' : forms.TextInput(attrs={'type':'text'}),
            'vendor' : forms.TextInput(attrs={'type':'text'}),
            'qty_per_unit' : forms.NumberInput(attrs={'type':'number'}),
            'discontinued' : forms.BooleanField(),
        }
        
class item_stock_form(ModelForm):
    class Meta:
        model = item_stock_model
        fields = ('__all__')
        widgets = {
            'itemChoice': forms.Select(),
            'date_updated': forms.DateInput(attrs={'type':'date'}),
            'exp_date': forms.DateInput(attrs={'type':'date'}),
            'cost_per_unit' : forms.NumberInput(attrs={'type':'number'}),
            'sell_price' : forms.NumberInput(attrs={'type':'number'}),
            'personal_stock' : forms.NumberInput(attrs={'type':'number'}),
        }
        
class machine_build_form(ModelForm):
    class Meta:
        model = machine_build_model
        fields = ('__all__')
        widgets = {
            'machineChoice': forms.Select(),
        }
        
class canta_payments_form(ModelForm):
    class Meta:
        model = canta_payments_model
        fields = ('__all__')
        widgets = {
            'machineChoice': forms.Select(),
            'gross_revenue': forms.NumberInput(attrs={'type':'float'}),
            'date': forms.DateInput(attrs={'type':'date'}),
        }
        
class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = [
            'phone_number',
            'property', 'unit_number',
            'lease_start_date', 'lease_end_date', 'monthly_rent', 'security_deposit',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'is_active', 'notes'
        ]

        # Adding widgets for better user experience
        widgets = {
            'property': forms.Select(attrs={}),
            'lease_start_date': forms.DateInput(attrs={'type': 'date'}),
            'lease_end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'monthly_rent': forms.NumberInput(attrs={'step': '0.01'}),
            'security_deposit': forms.NumberInput(attrs={'step': '0.01'}),
        }

        # Adding labels (optional, for clarity in forms)
        labels = {
            'phone_number': 'Phone Number',
            'property': 'Assigned Property',
            'unit_number': 'Unit Number (if applicable)',
            'lease_start_date': 'Lease Start Date',
            'lease_end_date': 'Lease End Date',
            'monthly_rent': 'Monthly Rent ($)',
            'security_deposit': 'Security Deposit ($)',
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_phone': 'Emergency Contact Phone',
            'emergency_contact_relationship': 'Emergency Contact Relationship',
            'is_active': 'Is Active?',
            'notes': 'Additional Notes',
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'name', 'address', 'city', 'state', 'zip_code',
            'owner_name', 'manager_name', 'manager_contact',
            'is_rental', 'rent_amount', 'lease_start_date', 'lease_end_date',
            'num_units', 'square_footage', 'year_built', 'notes',
            'is_active', 'maintenance_contact', 'maintenance_phone'
        ]

        widgets = {
            'lease_start_date': forms.DateInput(attrs={'type': 'date'}),
            'lease_end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'rent_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'square_footage': forms.NumberInput(attrs={'step': '1'}),
            'year_built': forms.NumberInput(attrs={'step': '1'}),
        }

        labels = {
            'name': 'Property Name',
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'zip_code': 'ZIP Code',
            'owner_name': 'Owner Name',
            'manager_name': 'Manager Name',
            'manager_contact': 'Manager Contact',
            'is_rental': 'Is Rental?',
            'rent_amount': 'Rent Amount ($)',
            'lease_start_date': 'Lease Start Date',
            'lease_end_date': 'Lease End Date',
            'num_units': 'Number of Units',
            'square_footage': 'Square Footage',
            'year_built': 'Year Built',
            'notes': 'Additional Notes',
            'is_active': 'Is Active?',
            'maintenance_contact': 'Maintenance Contact',
            'maintenance_phone': 'Maintenance Phone',
        }

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = WriteOff
        fields = ['transaction_type', 'category', 'amount', 'description', 'date', 'added_by']

        widgets = {
            'transaction_type': forms.Select(attrs={}),
            'category': forms.Select(attrs={}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

        labels = {
            'transaction_type': 'Transaction Type',
            'category': 'Expense Category',
            'amount': 'Amount ($)',
            'description': 'Description',
            'date': 'Date of Expense',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].choices = [('Expense', 'Expense')]  # Restrict to 'Expense' only
        self.fields['category'].choices = [
            ('auto', 'Auto Expenses'),
            ('business', 'Business Expenses'),
            ('home_office', 'Home Office Expenses'),
            ('meals', 'Meal Expenses'),
            ('property', 'Property Expenses')
        ]

class AddIncomeForm(forms.ModelForm):
    class Meta:
        model = WriteOff
        fields = ['transaction_type', 'category', 'amount', 'description', 'date', 'added_by']

        widgets = {
            'transaction_type': forms.Select(attrs={}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        labels = {
            'transaction_type': 'Transaction Type',
            'category': 'Category',
            'amount': 'Amount',
            'description': 'Description',
            'date': 'Date',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['transaction_type'].choices = [('Income', 'Income')]  # Restrict to 'Income' only
        self.fields['category'].choices = [
            ('house_sold', 'House Sold'),
            ('tax_return', 'Tax Return')
        ]

class MaintenanceRequestForm(forms.ModelForm):
    apply_month = forms.CharField(
        label="Apply to Month",
        widget=forms.TextInput(attrs={"type": "month"}),
        required=True,
        help_text="Which month this payment counts toward."
    )
    class Meta:
        model = MaintenanceRequest
        fields = ['category', 'description', 'status', 'property']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the issue', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'property': forms.Select(attrs={}),
        }

        labels = {
            'category': 'Select Category',
            'description': 'Description',
            'status': 'Status',
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'description', 'category']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter amount'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description (optional)', 'rows': 4}),
        }

        labels = {
            'category': 'Transaction Category',
            'transaction_type': 'Transaction Type',
            'amount': 'Amount ($)',
            'description': 'Description',
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LossStockForm(forms.ModelForm):
    machine_id = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        itemID = kwargs.pop('itemID', None)  # Get itemID if provided
        super(LossStockForm, self).__init__(*args, **kwargs)

        
        if itemID:
            machines_with_item = find_machines_with_item(itemID)
            
            machine_choices = [("", "Select a machine")]  # Blank option at the top
            
            # Only assign choices if machines exist
            if machines_with_item:
                machine_choices += [
                    (m["machine"], f"{m['machine']} (Lane {m['lane']})") for m in machines_with_item
                ]
            else:
                machine_choices.append(("", "No machines available"))

            self.fields["machine_id"].choices = machine_choices  # Assign filtered choices
    
    class Meta:
        model = LossStockModel
        fields = ["item_stock", "qty_of_item", "reason", "reported_by", "machine_id"]
        widgets = {
            "item_stock": forms.Select(attrs={"class": "form-control"}),
            "qty_of_item": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "reported_by": forms.TextInput(attrs={"class": "form-control"}),
            "machine_id": forms.Select(attrs={"class": "form-control"}),  # Dropdown for machine_id
        }

class MemberDuesPaymentForm(forms.ModelForm):
    apply_month = forms.CharField(
        label="Apply to Month",
        widget=forms.TextInput(attrs={"type": "month"}),
        required=True,
        help_text="Which month this payment counts toward."
    )

    class Meta:
        model = MemberDuesPayment
        fields = ["member", "amount", "paid_date", "note", "apply_month"]  # keep dues_month OUT of fields
        widgets = {
            "paid_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_apply_month(self):
        raw = (self.cleaned_data.get("apply_month") or "").strip()
        print(raw)
        # Expect "YYYY-MM"
        try:
            year_str, month_str = raw.split("-")
            y = int(year_str)
            m = int(month_str)
            return date(y, m, 1)
        except Exception:
            raise forms.ValidationError("Pick a valid month.")

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.dues_month = self.cleaned_data["apply_month"]
        if commit:
            obj.save()
        return obj
    











