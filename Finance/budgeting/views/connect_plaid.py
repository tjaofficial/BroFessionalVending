from django.shortcuts import render, redirect
from ..plaid_services import get_plaid_link_token, get_transactions, client
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import UserProfile, Transaction
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from django.views.decorators.csrf import csrf_exempt
from plaid.model.transactions_get_request import TransactionsGetRequest
from datetime import date, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages


@login_required
def connect_bank(request):
    link_token = get_plaid_link_token(request.user.id)
    return render(request, "bank/connect_bank.html", {"link_token": link_token})

def fetch_transactions(request):
    if not hasattr(request.user, 'user_profile') or not request.user.user_profile.plaid_access_token:
        return JsonResponse({"message": "No linked bank account!", "status": "error"}, status=400)

    access_token = request.user.user_profile.plaid_access_token

    try:
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()

        request_data = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            options={"count": 100}
        )

        response = client.transactions_get(request_data)
        transactions = response.to_dict().get('transactions', [])

        large_transactions = []  # ✅ Store large transactions for notification

        for txn in transactions:
            transaction, created = Transaction.objects.update_or_create(
                transaction_id=txn['transaction_id'],
                user=request.user,
                defaults={
                    "name": txn['name'],
                    "amount": txn['amount'],
                    "date": txn['date'],
                    "category": txn['category'][0] if txn.get('category') else "Uncategorized"
                }
            )

            # ✅ Check if the transaction is large
            if txn['amount'] > settings.LARGE_TRANSACTION_THRESHOLD:
                large_transactions.append(txn)

        # ✅ Trigger Notification if Large Transactions Exist
        if large_transactions:
            send_large_transaction_alert(request.user, large_transactions)

        return JsonResponse({"message": f"Fetched {len(transactions)} transactions and saved them!", "status": "success"})

    except Exception as e:
        return JsonResponse({"message": str(e), "status": "error"}, status=400)

@csrf_exempt
def exchange_public_token(request):
    if request.method == "POST":
        public_token = request.POST.get("public_token")

        try:
            request_data = ItemPublicTokenExchangeRequest(public_token=public_token)
            exchange_response = client.item_public_token_exchange(request_data)
            access_token = exchange_response['access_token']

            # ✅ Ensure the user profile exists before saving the access_token
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.plaid_access_token = access_token
            profile.save()

            return JsonResponse({"message": "Bank account linked successfully!", "status": "success"})

        except Exception as e:
            return JsonResponse({"message": str(e), "status": "error"}, status=400)


def send_large_transaction_alert(user, large_transactions):
    """ Sends an alert when large transactions are detected. """
    
    # ✅ Create the alert message
    transaction_details = "\n".join(
        [f"{txn['date']}: {txn['name']} - ${txn['amount']}" for txn in large_transactions]
    )

    subject = "🚨 Large Transaction Alert 🚨"
    message = f"Hey {user.username},\n\nThe following large transactions were detected in your account:\n\n{transaction_details}\n\nPlease review them to ensure they're correct."

    # ✅ Send email alert
    send_mail(
        subject,
        message,
        'brofessionalvending@gmail.com',  # ✅ Replace with your actual email sender
        [user.email],
        fail_silently=False,
    )

    print(f"📩 Large Transaction Alert Sent to {user.email}")
