from django_cron import CronJobBase, Schedule #type: ignore
from datetime import date #type: ignore
import stripe #type: ignore
from django.conf import settings #type: ignore
from .models import Transaction, Tenant
from decimal import Decimal
from django.utils import timezone #type: ignore
from datetime import datetime
from .utils import first_of_month


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
    RUN_EVERY_MINS = 1440  # once per day
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "monthly_bills.charge_monthly_rent"

    def do(self):
        today = timezone.localdate()
        rent_month = first_of_month(today)

        # Optional: only charge on the 1st
        if today.day != 1:
            print("[RentCron] Skipping — not the 1st of the month.")
            return

        tenants = Tenant.objects.select_related(
            "userProf", "userProf__user"
        ).filter(is_active=True)

        if not tenants.exists():
            print("[RentCron] No active tenants.")
            return

        created = 0
        skipped = 0

        for tenant in tenants:
            # Safety checks
            if not tenant.userProf:
                skipped += 1
                continue

            # Lease window check
            if tenant.lease_start_date > rent_month:
                skipped += 1
                continue

            if tenant.lease_end_date < rent_month:
                skipped += 1
                continue

            # 🔐 Idempotency check
            already_exists = Transaction.objects.filter(
                tenantChoice=tenant,
                transaction_type="Charge",
                category="Rent",
                rent_month=rent_month,
            ).exists()

            if already_exists:
                skipped += 1
                continue

            Transaction.objects.create(
                tenant=tenant.userProf,
                tenantChoice=tenant,
                transaction_type="Charge",
                category="Rent",
                amount=Decimal(tenant.monthly_rent),
                description=f"Monthly rent charge ({rent_month.strftime('%B %Y')})",
                status="Completed",
                rent_month=rent_month,
            )

            created += 1
            print(f"[RentCron] Charged {tenant.userProf.user.get_full_name()} — ${tenant.monthly_rent}")

        print(f"[RentCron] Done. Created={created}, Skipped={skipped}")