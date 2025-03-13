from django_cron import CronJobBase, Schedule
from .models import UserProfile, Transaction
from .plaid_services import get_transactions

class FetchTransactionsCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 * 24  # Run once per day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "budgeting.FetchTransactionsCronJob"  # ✅ Correct class name

    def do(self):
        print("🔄 Running FetchTransactionsCronJob...")  # Debugging line

        profiles = UserProfile.objects.exclude(plaid_access_token__isnull=True).exclude(plaid_access_token="")

        print(f"👤 Found {profiles.count()} profiles with linked bank accounts.")  # Debugging line

        for profile in profiles:
            access_token = profile.plaid_access_token
            transactions = get_transactions(access_token)

            print(f"📥 Fetched {len(transactions)} transactions for {profile.user.username}")  # Debugging line

            for txn in transactions:
                Transaction.objects.update_or_create(
                    transaction_id=txn['transaction_id'],
                    user=profile.user,
                    defaults={
                        "name": txn['name'],
                        "amount": txn['amount'],
                        "date": txn['date'],
                        "category": txn['category'][0] if txn.get('category') else "Uncategorized"
                    }
                )

        print(f"✅ Successfully fetched transactions for {profiles.count()} users.")
