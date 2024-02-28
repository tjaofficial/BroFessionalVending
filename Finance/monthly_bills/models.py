from django.db import models

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
    
class inventory_sheets_model(models.Model):
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
    data = models.CharField(
        max_length=10000,
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
    container_description = models.CharField(
        max_length=60
    )
    vendor = models.CharField(
        max_length=30
    )
    qty_per_unit = models.IntegerField()
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
    sell_price = models.FloatField()
    cost_per_unit = models.FloatField()
    personal_stock = models.IntegerField()
    
    def __str__(self):
        return str(self.itemChoice.itemID) + ' - ' + str(self.date_updated)
    
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
        return str(self.machineChoice)
    
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
    
    
    
    