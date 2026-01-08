from django.db import models #type: ignore
from django.contrib.auth.models import User #type: ignore
from datetime import date, timedelta

# Create your models here.

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    category = models.CharField(max_length=100, choices=[
        ('Job', 'Job'),
        ('Side Hustle', 'Side Hustle'),
        ('Passive Income', 'Passive Income')
    ])

    def __str__(self):
        return f"{self.source} - ${self.amount}" 

CATEGORY_CHOICES = [
    ('Groceries', 'Groceries'),
    ('Gas', 'Gas'),
    ('Rent', 'Rent'),
    ('Utilities', 'Utilities'),
    ('Entertainment', 'Entertainment'),
    ('Dining', 'Dining'),
    ('Shopping', 'Shopping'),
    ('Health', 'Health'),
    ('Transportation', 'Transportation'),
    ('Other', 'Other'),
]

# Keywords for Auto-Categorization
CATEGORY_KEYWORDS = {
    'Groceries': ['walmart', 'kroger', 'meijer', 'costco', 'aldi'],
    'Gas': ['shell', 'bp', 'marathon', 'mobil', 'exxon', 'chevron'],
    'Rent': ['apartment', 'rent', 'landlord'],
    'Utilities': ['dte', 'water bill', 'comcast', 'internet', 'at&t'],
    'Entertainment': ['netflix', 'spotify', 'hulu', 'theater'],
    'Dining': ['mcdonalds', 'taco bell', 'pizza', 'restaurant', 'burger king'],
    'Shopping': ['amazon', 'best buy', 'target'],
    'Health': ['pharmacy', 'doctor', 'hospital', 'cvs', 'walgreens'],
    'Transportation': ['uber', 'lyft', 'bus', 'subway', 'metro'],
}

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Other')
    is_recurring = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.category = self.auto_categorize(self.description)
        super().save(*args, **kwargs)

    def auto_categorize(self, description):
        description_lower = description.lower()
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        return 'Other'

    def __str__(self):
        return f"{self.description} - ${self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    current_spending = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.category} Budget: ${self.limit}" 

class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creditor = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_payment = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.FloatField()

    def __str__(self):
        return f"{self.creditor} - ${self.balance}" 

class Savings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=255)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    target_date = models.DateField()

    def __str__(self):
        return f"{self.goal_name} - ${self.current_amount}/${self.goal_amount}" 

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_date = models.DateField()
    payment_link = models.URLField()

    def __str__(self):
        return f"{self.card_name} - ${self.balance}"


class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_recurring = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=[
        ('Rent', 'Rent'),
        ('Utilities', 'Utilities'),
        ('Credit Card', 'Credit Card'),
        ('Loan', 'Loan'),
        ('Subscription', 'Subscription'),
        ('Other', 'Other')
    ], default='Other')

    def is_due_soon(self):
        return self.due_date <= date.today() + timedelta(days=7)

    def __str__(self):
        return f"{self.name} - Due: {self.due_date} - ${self.amount}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    plaid_access_token = models.CharField(max_length=255, blank=True, null=True)
    alert_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)  # ✅ Default global threshold
    category_thresholds = models.JSONField(default=dict, blank=True, null=True)  # ✅ Category-specific thresholds

    def get_threshold_for_category(self, category):
        """ Returns the threshold for a specific category or default if not set """
        return self.category_thresholds.get(category, self.alert_threshold)

    def set_threshold_for_category(self, category, threshold):
        """ Sets a threshold for a specific category """
        thresholds = self.category_thresholds or {}
        thresholds[category] = threshold
        self.category_thresholds = thresholds
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=255, blank=True, null=True)
    ai_predicted_category = models.CharField(max_length=255, blank=True, null=True)  # ✅ New field for AI predictions
    dismissed = models.BooleanField(default=False)
    ai_accuracy = models.FloatField(blank=True, null=True)  # ✅ Track AI confidence
    ai_approved = models.BooleanField(default=False)  # ✅ Whether user accepted the AI's prediction    

    def __str__(self):
        return f"{self.name} - ${self.amount} on {self.date}"
