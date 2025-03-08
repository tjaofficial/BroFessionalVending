from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
bill_categories = (
    ('Automotive', 'Automotive'),
    ('Food', 'Food'),
    ('Phone', 'Phone'),
    ('Rent', 'Rent'),
    ('Studio', 'Studio'),
    ('Music', 'Music'),
    ('Alcohol', 'Alcohol'),
    ('Vending', 'Vending'),
    ('Extra', 'Extra'),
    ('Personal', 'Personal'),
)
vending_categories = (
    ('Automotive', 'Automotive'),
    ('Meetings', 'Meetings'),
    ('Gas', 'Gas'),
    ('Equipment', 'Equipment'),
    ('Restock', 'Restock'),
    ('Repairs', 'Repairs'),
    ('Income', 'Income'),
    ('Other', 'Other'),
)
vendType = (
    ('Snack', 'Snack Machine'),
    ('Brand Drink', 'Brand Drink Machine'),
    ('Combination', 'Combination Machine'),
    ('Glass Front Drink', 'Glass Front Drink Machine'),
    ('Satallite Drink', 'Satallite Drink Machine'),
    ('Satallite Snack', 'Satallite Snack Machine'),
)
conditions = (
    ('Needs Maintenance ','Needs Maintenance '),
    ('Very Poor','Very Poor'),
    ('Poor','Poor'),
    ('Satisfactory','Satisfactory'),
    ('Great','Great'),
)
product_choice = (
    ('Snack', 'Snack Machine'),
    ('Drink', 'Drink Machine'),
    ('Combination', 'Combination Machine'),
)
billing_periods = (
    ('Annually', 'Annually'),
    ('Semi-Annually', 'Semi-Annually'),
    ('Quarterly', 'Quarterly'),
    ('Monthly', 'Monthly'),
    ('Bi-Monthly', 'Bi-Monthly'),
    ('Weekly', 'Weekly'),
)
class bill_items_model(models.Model):
    title = models.CharField(
        max_length=30
    )
    budget_amt = models.DecimalField(
        max_digits=6, 
        decimal_places=2
    )
    est_date = models.DateField(
        auto_now_add=False, 
        auto_now=False,
        null= True,
        blank = True
    )
    category = models.CharField(
        max_length=30,
        choices = bill_categories
    )
    monthly_period = models.IntegerField()
    
    def __str__(self):
        return str(self.est_date) + ' - ' + self.title

class bills_model(models.Model):
    title = models.CharField(
        max_length=30
    )
    budget_amt = models.DecimalField(
        max_digits=6, 
        decimal_places=2
    )
    charge_day_1 = models.IntegerField()
    category = models.CharField(
        max_length=30,
        choices = bill_categories
    )
    billing_period = models.CharField(
        max_length=30,
        choices = billing_periods
    )
    charge_day_2 = models.IntegerField(
        null= True,
        blank = True
    )
    source = models.CharField(
        max_length=30
    )
    start_date = models.DateField(
        auto_now_add=False, 
        auto_now=False,
        null= True,
        blank = True
    )
    stop_date = models.DateField(
        auto_now_add=False, 
        auto_now=False,
        null= True,
        blank = True
    )
    
    def __str__(self):
        return str(self.start_date) + ' - ' + self.title
    
class pay_log(models.Model):
    bill = models.CharField(
        max_length=30,
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False,
        null= True,
        blank = True
    )
    payment = models.DecimalField(
        max_digits=6, 
        decimal_places=2
    )
    
    def __str__(self):
        return str(self.date) + ' - ' + self.bill
    
class income_log(models.Model):
    income = (
        ('first','1st'),
        ('second','2nd'),
        ('expense','Expense'),
        ('music','Music'),
        ('extra','Extra')
        
    )
    title = models.CharField(
        max_length=30,
        choices = income
    )
    describe = models.CharField(
        max_length=30,
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False
    )
    amount = models.DecimalField(
        max_digits=6, 
        decimal_places=2
    )
    
    def __str__(self):
        return str(self.date)

class purchase_model(models.Model):
    title = models.CharField(
        max_length=30
    )
    amount = models.DecimalField(
        max_digits=6, 
        decimal_places=2
    )
    date = models.DateField(
        auto_now_add=False, 
        auto_now=False
    )
    category = models.CharField(
        max_length=30,
        choices = bill_categories
    )
    
    def __str__(self):
        return str(self.date) + ' - ' + self.title
    
class machine_model_model(models.Model):
    model_number = models.CharField(max_length=70)
    type = models.CharField(max_length=40)
    glass_front = models.BooleanField()
    satallite = models.BooleanField()
    def __str__(self):
        return str(self.model_number)
    
class fleet_model(models.Model):
    id_tag = models.CharField(
        max_length=7,
    )
    machine_type = models.CharField(
        max_length=30,
        choices = vendType
    )
    model= models.CharField(
        max_length=30,
    )
    key_id = models.CharField(
        max_length=10,
    )
    serial_num = models.CharField(
        max_length=15,
    )
    buy_price = models.IntegerField()
    date_bought = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    location_name = models.CharField(
        max_length=30,
    )
    address = models.CharField(
        max_length=60,
    )
    contact_name = models.CharField(
        max_length=30,
    )
    phone = models.CharField(
        max_length=10,
    )
    in_service = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True
    )
    last_service = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True        
    )
    next_servicing = models.DateField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True
    )
    notes = models.CharField(
        max_length=600
    )
    active = models.BooleanField(
        default=False,
        null=True
    )
    modelChoice = models.ForeignKey(
        to=machine_model_model, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.id_tag
    
class machine_stock_model(models.Model):
    id_tag = models.ForeignKey(to=fleet_model, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=30
    )
    size = models.CharField(
        max_length=30
    )
    cost_per_unit = models.FloatField()
    sell_price = models.FloatField()
    vendor = models.CharField(
        max_length=30
    )
    qty_per_unit = models.IntegerField()
    in_stock = models.IntegerField()
    discontinued = models.BooleanField(
        default=False,
        null=True
    )
    itemID = models.CharField(
        max_length=15
    )
    
    def __str__(self):
        return str(self.id_tag.id_tag) + ' - ' + str(self.name)
    
class vmax576_model(models.Model):
    business = models.CharField(
        max_length=30
    )
    id_tag = models.ForeignKey(to=fleet_model, on_delete=models.CASCADE)
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    time_start = models.TimeField(
        auto_now=False, 
        auto_now_add=False
    )
    time_end = models.TimeField(
        auto_now=False, 
        auto_now_add=False
    )
    technician = models.CharField(
        max_length=30,
    )
    condition = models.CharField(
        max_length=30,
        choices=conditions,
    )
    collected = models.FloatField()
    
    lane_1 = models.JSONField(
        null=True,
        blank=True
    )

    lane_2 = models.JSONField(
        null=True,
        blank=True
    )

    lane_3 = models.JSONField(
        null=True,
        blank=True
    )

    lane_4 = models.JSONField(
        null=True,
        blank=True
    )

    lane_5 = models.JSONField(
        null=True,
        blank=True
    )

    lane_6 = models.JSONField(
        null=True,
        blank=True
    )
    
    lane_7 = models.JSONField(
        null=True,
        blank=True
    )

    lane_8 = models.JSONField(
        null=True,
        blank=True
    )
    def __str__(self):
        return str(self.date)
     
class RS900_model(models.Model):
    business = models.CharField(
        max_length=30
    )
    id_tag = models.ForeignKey(to=fleet_model, on_delete=models.CASCADE)
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    time_start = models.TimeField(
        auto_now=False, 
        auto_now_add=False
    )
    time_end = models.TimeField(
        auto_now=False, 
        auto_now_add=False
    )
    technician = models.CharField(
        max_length=30,
    )
    condition = models.CharField(
        max_length=30,
        choices=conditions,
    )
    collected = models.FloatField()
    
    A1 = models.CharField(
        max_length=300,
    )
    A2 = models.CharField(
        max_length=300,
    )
    A3 = models.CharField(
        max_length=300,
    )
    A4 = models.CharField(
        max_length=300,
    )
    A5 = models.CharField(
        max_length=300,
    )
    
    B1 = models.CharField(
        max_length=300,
    )
    B2 = models.CharField(
        max_length=300,
    )
    B3 = models.CharField(
        max_length=300,
    )
    B4 = models.CharField(
        max_length=300,
    )
    B5 = models.CharField(
        max_length=300,
    )
    B6 = models.CharField(
        max_length=300,
    )
    
    C1 = models.CharField(
        max_length=300,
    )
    C2 = models.CharField(
        max_length=300,
    )
    C3 = models.CharField(
        max_length=300,
    )
    C4 = models.CharField(
        max_length=300,
    )
    C5 = models.CharField(
        max_length=300,
    )
    C6 = models.CharField(
        max_length=300,
    )
    C7 = models.CharField(
        max_length=300,
    )
    C8 = models.CharField(
        max_length=300,
    )
    C9 = models.CharField(
        max_length=300,
    )
    C10 = models.CharField(
        max_length=300,
    )
    
    D1 = models.CharField(
        max_length=300,
    )
    D2 = models.CharField(
        max_length=300,
    )
    D3 = models.CharField(
        max_length=300,
    )
    D4 = models.CharField(
        max_length=300,
    )
    D5 = models.CharField(
        max_length=300,
    )
    D6 = models.CharField(
        max_length=300,
    )
    D7 = models.CharField(
        max_length=300,
    )
    D8 = models.CharField(
        max_length=300,
    )
    
    def __str__(self):
        return str(self.date)
       
class machine_database_model(models.Model):
    type = models.CharField(
        max_length=30,
        choices=product_choice
    )
    brand = models.CharField(
        max_length=30,
    )
    model_num = models.CharField(
        max_length=30,
    )
    drink_slots = models.IntegerField()
    snack_slots = models.IntegerField()
    
    def __str__(self):
        return self.model_num
    
class gas_log_model(models.Model):
    name = models.CharField(
        max_length=30,
    )
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    actual_cost = models.FloatField()
    description = models.CharField(
        max_length=600
    )
    def __str__(self):
        return str(self.date)
    
class mileage_log_model(models.Model):
    name = models.CharField(
        max_length=30,
    )
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    mileage = models.FloatField()
    description = models.CharField(
        max_length=600
    )
    def __str__(self):
        return str(self.date)
    
class machine_build_model(models.Model):
    machineChoice = models.ForeignKey(
        to=fleet_model, 
        on_delete=models.CASCADE,
    )
    slot_dictionary = models.JSONField()
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    def __str__(self):
        return str(self.machineChoice) + ' - ' + str(self.date)

class inventory_sheets_model(models.Model):
    business = models.CharField(
        max_length=30
    )
    id_tag = models.ForeignKey(to=fleet_model, on_delete=models.CASCADE)
    machineBuild = models.ForeignKey(
        to=machine_build_model, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    time_start = models.TimeField(
        auto_now=False, 
        auto_now_add=False
    )
    time_end = models.TimeField(
        auto_now=False, 
        auto_now_add=False
    )
    technician = models.CharField(
        max_length=30,
    )
    condition = models.CharField(
        max_length=30,
        choices=conditions,
    )
    collected = models.FloatField()
    data = models.JSONField(
        default=dict
    )
    general_notes = models.CharField(max_length=10000, default='none')
    def __str__(self):
        return str(self.date) + ' - ' + str(self.id_tag.id_tag)
    
class vending_finance(models.Model):
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    transaction = models.CharField(
        max_length=300
    )
    withdrawal = models.FloatField(
        null= True,
        blank = True
    )
    deposit = models.FloatField(
        null= True,
        blank = True
    )
    category = models.CharField(
        max_length=30,
        choices = vending_categories
    )
    def __str__(self):
        return str(self.date) + ' - ' + str(self.transaction)
    
class price_model(models.Model):
    machine_id = models.CharField(
        max_length=20
    )
    price_JSON = models.CharField(
        max_length=3000000
    )
    def __str__(self):
        return self.machine_id
    
class cantaLogs_model(models.Model):
    id_tag = models.ForeignKey(to=fleet_model, on_delete=models.CASCADE)
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    prev_count = models.CharField(
        max_length=3000000
    )
    adding = models.CharField(
        max_length=3000000
    )
    sold = models.CharField(
        max_length=3000000
    )
    def __str__(self):
        return str(self.date) + ' - ' + str(self.id_tag)
    
class FAQ_model(models.Model):
    section = models.CharField(max_length=75)
    question = models.CharField(max_length=150)
    answer = models.CharField(max_length=700)
    link = models.CharField(
        max_length=30,
        null=True, 
        blank=True
    )
    def __str__(self):
        return str(self.question)
    
class item_data_model(models.Model):
    typePrimeChoices = (
        ('drinks','drinks'),
        ('snacks','snacks'),
    )
    typeChoices = (
        ('candy','candy'),
        ('chips','chips'),
        ('health bars','health bars'),
        ('meat sticks','meat sticks'),
        ('energy drinks','energy drinks'),
        ('soda pops','soda pops'),
        ('juices','juices'),
        ('crackers','crackers'),
        ('cookies','cookies'),
        ('water','water'),
    )
    name = models.CharField(
        max_length=30
    )
    itemPrimaryType =  models.CharField(
        max_length=60,
        choices=typePrimeChoices
    )
    itemSecondaryType =  models.CharField(
        max_length=60,
        choices=typeChoices
    )
    discontinued = models.BooleanField(
        default=False,
        null=True
    )
    itemID = models.CharField(
        max_length=15
    )
    def __str__(self):
        return str(self.itemID) + ' - ' + str(self.name)
    
class item_stock_model(models.Model):
    itemChoice = models.ForeignKey(to=item_data_model, on_delete=models.CASCADE)
    date_updated = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    exp_date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    cost_per_unit = models.FloatField()
    qty_per_unit = models.IntegerField()
    vendor = models.CharField(
        max_length=30
    )
    qty_of_units = models.IntegerField(
        default=1
    )
    
    def __str__(self):
        return str(self.itemChoice.itemID) + ' - ' + str(self.date_updated)
    
class canta_payments_model(models.Model):
    machineChoice = models.ForeignKey(
        to=fleet_model, 
        on_delete=models.CASCADE,
    )
    gross_revenue = models.FloatField()
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    def __str__(self):
        return str(self.date) + " - " + str(self.machineChoice)
    
class Tenant(models.Model):
    # Basic Personal Details
    userProf = models.ForeignKey('UserProfile', on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=15)

    # Address Details
    property = models.ForeignKey(
        'Property',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tenants'
    )
    unit_number = models.CharField(max_length=10, blank=True, null=True)  # Optional
    # Lease Details
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)

    # Additional Details
    is_active = models.BooleanField(default=True)  # Whether the tenant is currently renting
    notes = models.TextField(blank=True, null=True)  # Optional field for additional notes

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Payment Profile
    stripe_payment_data = models.ForeignKey(
        'PaymentMethod',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.userProf} ({self.property.address})"

class Property(models.Model):
    # Basic Property Details
    name = models.CharField(max_length=100)  # Name or identifier for the property
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, default='Michigan')  # Default to Michigan
    zip_code = models.CharField(max_length=10)

    # Ownership and Management
    owner_name = models.CharField(max_length=100, blank=True, null=True)  # Optional
    manager_name = models.CharField(max_length=100, blank=True, null=True)
    manager_contact = models.CharField(max_length=15, blank=True, null=True)

    # Rental Details
    is_rental = models.BooleanField(default=True)  # Whether the property is rented out
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lease_start_date = models.DateField(blank=True, null=True)
    lease_end_date = models.DateField(blank=True, null=True)
    tenant = models.ForeignKey(
        'Tenant', on_delete=models.SET_NULL, blank=True, null=True, related_name='properties'
    )  # Optional link to a tenant

    # Property Features
    num_units = models.IntegerField(default=1)  # For multi-unit properties
    square_footage = models.PositiveIntegerField(blank=True, null=True)  # Optional
    year_built = models.PositiveIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)  # Additional property details

    # Maintenance and Status
    is_active = models.BooleanField(default=True)  # Whether the property is active in portfolio
    maintenance_contact = models.CharField(max_length=100, blank=True, null=True)
    maintenance_phone = models.CharField(max_length=15, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.address})"

class WriteOff(models.Model):
    CATEGORY_CHOICES = [
        ('auto', 'Auto Expenses'),
        ('business', 'Business Expenses'),
        ('home_office', 'Home Office Expenses'),
        ('meals', 'Meal Expenses'),
        ('property', 'Property Expenses'),
        ('rent', 'Rent'),
        ('house_sold', 'House Sold'),
        ('deposit', 'Deposit'),
        ('tax_return', 'Tax Return')
    ]

    TRANSACTION_TYPE_CHOICES = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, default='Expense')
    last_updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='writeoffs',null=True,  # Allow null temporarily
    blank=True)

    def __str__(self):
        return f"{self.get_category_display()} - ${self.amount} on {self.date}"

class Revenue(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"${self.amount} on {self.date}"

class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    MAINTENANCE_CATEGORY = [
        ('Appliance', 'Appliance'),
        ('Doors and locks', 'Doors and locks'),
        ('Electrical and lighting', 'Electrical and lighting'),
        ('Flooring', 'Flooring'),
        ('General', 'General'),
        ('Heating and cooling', 'Heating and cooling'),
        ('Plumbing and bath', 'Plumbing and bath'),
        ('Safety equipment', 'Safety equipment'),
        ('Preventative Maintenance', 'Preventative Maintenance'),
    ]

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maintenance_requests')
    category = models.CharField(max_length=40, choices=MAINTENANCE_CATEGORY, default='General')
    property = models.ForeignKey(
        'Property',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} ({self.status}) - {self.tenant.username}"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Charge', 'Charge'),
        ('Payment', 'Payment'),
    ]

    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Fee', 'Fee'),
        ('Deposit', 'Deposit'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Scheduled', 'Scheduled'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
        ('Canceled', 'Canceled'),
    ]

    tenant = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='transactions')
    tenantChoice = models.ForeignKey('Tenant', on_delete=models.CASCADE, blank=True, null=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Other")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, blank=True, null=True)
    scheduled_date = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - ${self.amount} for {self.tenant.user.username} on {self.date.strftime('%Y-%m-%d')}"

class UserProfile(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ('Vending', 'Vending'),
        ('Legacy', 'Legacy'),
        ('Tenant', 'Tenant'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.business_type})"

class TransactionCharge(models.Model):
    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Fee', 'Fee'),
        ('Deposit', 'Deposit'),
        ('Other', 'Other'),
    ]

    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Other")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    is_paid = models.BooleanField(default=False)  # New field to indicate payment status

    def __str__(self):
        return f"Charge - ${self.amount} for {self.tenant.username} on {self.date.strftime('%Y-%m-%d')}"
    
class TransactionPayment(models.Model):
    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Fee', 'Fee'),
        ('Deposit', 'Deposit'),
        ('Other', 'Other'),
    ]
    transaction_charge = models.ForeignKey('TransactionCharge', on_delete=models.SET_NULL, related_name='transactionsPayment', blank=True, null=True)
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Other")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment - ${self.amount} for {self.tenant.username} on {self.date.strftime('%Y-%m-%d')}"
    
class home_inventory_model(models.Model):
    item = models.OneToOneField(item_data_model, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    log = models.TextField(default="", blank=True)  # Stores update history

    def update_stock(self, change, action):
        """
        Updates stock and appends changes to log.
        change: Number of items added (+) or removed (-)
        action: Description of what happened (e.g., "Restocked", "Added to machine")
        """
        old_qty = self.quantity
        self.quantity += change
        self.log += f"\n{timezone.now().strftime('%Y-%m-%d %H:%M:%S')} - {action}: {old_qty} → {self.quantity} (Change: {change})"
        self.save()

    def __str__(self):
        return f"{self.item.name} - {self.quantity} at home"

class LossStockModel(models.Model):
    item_stock = models.ManyToManyField("item_stock_model", related_name="loss_records")
    qty_of_item = models.PositiveIntegerField(default=0)  # Quantity lost
    reason = models.TextField()  # Reason for loss
    date = models.DateField(auto_now_add=True)  # Date of loss
    reported_by = models.CharField(max_length=50, blank=True, null=True)  # Who reported the loss
    machine_id = models.CharField(max_length=30, blank=True, null=True)  # If loss happened in a specific machine

    def __str__(self):
        return f"Loss on {self.date} - {self.qty_of_item} units"
    
class PaymentMethod(models.Model):
    tenantChoice = models.OneToOneField("Tenant", on_delete=models.CASCADE, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_payment_method_id = models.CharField(max_length=255, null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    brand = models.CharField(max_length=50, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} ending in {self.last4} for {self.tenantChoice}"







