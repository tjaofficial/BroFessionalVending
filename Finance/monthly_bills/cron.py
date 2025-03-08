from django_cron import CronJobBase, Schedule
from datetime import date
import stripe
from django.conf import settings
from .models import Transaction, Tenant
from decimal import Decimal
from django.utils import timezone
from datetime import datetime


class ProcessScheduledPayments(CronJobBase):
    stripe.api_key = settings.STRIPE_SECRET_KEY  # Set Stripe API Key
    RUN_EVERY_MINS = 1440  # 1440 minutes = 1 day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "monthly_bills.process_scheduled_payments"  # Unique code

    def do(self):
        today = date.today()
        scheduled_payments = Transaction.objects.filter(status="Scheduled", scheduled_date=today)

        if not scheduled_payments.exists():
            print("✅ No scheduled payments for today.")
            return

        for payment in scheduled_payments:
            try:
                stripe.PaymentIntent.create(
                    amount=int(Decimal(payment.amount) * 100),  # Convert to cents
                    currency="usd",
                    payment_method=payment.payment_method.stripe_payment_method_id,
                    confirm=True,
                    customer=payment.payment_method.stripe_customer_id,
                    description="Scheduled Rent Payment"
                )
                payment.status = "Completed"
                payment.save()
                print(f"✅ Payment of ${payment.amount} processed for {payment.tenant.userProf.user.username}")
            
            except stripe.error.CardError as e:
                payment.status = "Failed"
                payment.save()
                print(f"❌ Payment failed for {payment.tenant.userProf.user.username}: {e.error.message}")

class ChargeMonthlyRentCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # 1440 minutes = 24 hours (runs once per day)
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'monthly_bills.charge_monthly_rent'  # Update with correct app name

    def do(self):
        today = timezone.now()

        # Only execute on the 1st of the month
        if today.day != 1:
            print("[Django-Cron] Skipping - Not the 1st of the month.")
            return

        first_day_of_month = timezone.make_aware(datetime(today.year, today.month, 1, 0, 0, 0))

        active_tenants = Tenant.objects.filter(is_active=True)

        if not active_tenants.exists():
            print("[Django-Cron] No active tenants found.")
            return

        for tenant in active_tenants:
            rent_amount = tenant.monthly_rent  # Ensure Tenant model has rent_amount field

            # Create a new rent charge transaction
            transaction = Transaction.objects.create(
                tenant=tenant.userProf,
                tenantChoice=tenant,
                transaction_type='Charge',
                category='Rent',
                amount=rent_amount,
                description=f"Monthly rent charge for {today.strftime('%B %Y')}",
                status='Completed',
                scheduled_date=first_day_of_month
            )

            print(f"[Django-Cron] Rent charge created for {tenant.user.username}: ${rent_amount}")


