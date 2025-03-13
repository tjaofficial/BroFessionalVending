from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api_client import ApiClient
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
import os
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from datetime import date, timedelta


# Plaid API Configuration
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

# Configure the client
configuration = Configuration(
    host=f"https://{PLAID_ENV}.plaid.com",
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET
    }
)

api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)


def get_plaid_link_token(user_id):
    """Generates a Plaid Link token for connecting a bank."""
    request = LinkTokenCreateRequest(
        user={"client_user_id": str(user_id)},
        client_name="BroFessional Vending Budgeting",
        products=[Products("transactions")],
        country_codes=[CountryCode("US")],
        language="en"
    )
    response = client.link_token_create(request)
    return response["link_token"]


def get_transactions(access_token):
    """ Fetches transactions from Plaid """
    start_date = date.now() - timedelta(days=30)
    end_date = date.now()

    try:
        request_data = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            count=100  # Optional: Limits the number of transactions retrieved
        )
        response = client.transactions_get(request_data)  # ✅ Corrected call
        return response.to_dict().get('transactions', [])
    except Exception as e:
        print(f"❌ Error fetching transactions: {e}")
        return []
