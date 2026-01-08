from django.shortcuts import render, redirect, get_object_or_404 #type: ignore
from ..forms import TenantForm, PropertyForm, AddExpenseForm, MaintenanceRequestForm, AddIncomeForm
from ..models import PaymentMethod, Property, Tenant, WriteOff, Revenue, MaintenanceRequest, Transaction, UserProfile
from ..utils import payment_charges_totals
from django.db.models import Sum #type: ignore
from django.db.models.functions import ExtractYear #type: ignore
from django.http import JsonResponse #type: ignore
from django.contrib.auth.decorators import login_required #type: ignore
from django.contrib.auth.forms import UserCreationForm #type: ignore
from django.contrib import messages #type: ignore
import stripe #type: ignore
from django.views.decorators.csrf import csrf_exempt #type: ignore
from django.conf import settings #type: ignore
import json
from datetime import datetime, date
from decimal import Decimal
from django.urls import reverse #type: ignore



@login_required
def add_tenant(request):
    userProf = UserProfile.objects.filter(business_type="Tenant")

    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            A = form.save(commit=False)
            A.userProf=userProf.get(id=request.POST['userProf'])
            A.save()
            return redirect('view_tenants')  # Replace with your tenant listing page
    else:
        form = TenantForm()
    return render(request,'legacy_lineage/add_tenant.html',{
        'form':form, 'userProf': userProf
    })

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_properties')  # Replace with your redirect page
    else:
        form = PropertyForm()
    return render(request, 'legacy_lineage/add_property.html', {
        'form': form
    })

@login_required
def view_properties(request):
    # Get query parameters for filtering
    city = request.GET.get('city', '').strip().lower()
    state = request.GET.get('state', '').strip().lower()
    tenant_name = request.GET.get('tenant', '').strip().lower()

    # Fetch all properties initially
    properties = Property.objects.all()

    # Apply filtering if query parameters are provided
    if city:
        properties = properties.filter(city__icontains=city)
    if state:
        properties = properties.filter(state__icontains=state)
    if tenant_name:
        properties = properties.filter(tenants__first_name__icontains=tenant_name) | \
                     properties.filter(tenants__last_name__icontains=tenant_name)

    # Pass the filtered properties to the template
    context = {
        'properties': properties
    }
    return render(request, 'legacy_lineage/view_properties.html', context)

@login_required
def view_tenants(request):
    # Get query parameters for filtering
    name = request.GET.get('name', '').strip().lower()
    city = request.GET.get('city', '').strip().lower()
    state = request.GET.get('state', '').strip().lower()

    # Fetch all tenants initially
    tenants = Tenant.objects.all()

    # Apply filtering based on query parameters
    if name:
        tenants = tenants.filter(user__first_name__icontains=name) | tenants.filter(user__last_name__icontains=name)
    if city:
        tenants = tenants.filter(city__icontains=city)
    if state:
        tenants = tenants.filter(state__icontains=state)

    # Pass the filtered tenants to the template
    context = {
        'tenants': tenants
    }
    return render(request, 'legacy_lineage/view_tenants.html', context)

# View: Display Overview of Write-Offs
@login_required
def expense_overview(request):
    # Calculate totals by category
    totals = {
        'auto': WriteOff.objects.filter(category='auto', transaction_type="Expense").aggregate(Sum('amount'))['amount__sum'] or 0,
        'business': WriteOff.objects.filter(category='business', transaction_type="Expense").aggregate(Sum('amount'))['amount__sum'] or 0,
        'home_office': WriteOff.objects.filter(category='home_office', transaction_type="Expense").aggregate(Sum('amount'))['amount__sum'] or 0,
        'meals': WriteOff.objects.filter(category='meals', transaction_type="Expense").aggregate(Sum('amount'))['amount__sum'] or 0,
        'property': WriteOff.objects.filter(category='property', transaction_type="Expense").aggregate(Sum('amount'))['amount__sum'] or 0,
        'income': WriteOff.objects.filter(category__in=["rent", "dues"], transaction_type="Income").aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    writeoffs = WriteOff.objects.all().order_by('-date')

    if request.method == 'POST':
        copy_request = request.POST.copy()
        copy_request['added_by'] = UserProfile.objects.get(user=request.user)
        if 'deleteButton' in request.POST.keys():
            writeoffInstance = WriteOff.objects.get(id=request.POST['writeOffId'])
            writeoffInstance.delete()
        else:
            if 'addExpenseButton' in request.POST.keys():
                form = AddExpenseForm(copy_request)
            elif 'addIncomeButton' in request.POST.keys():
                form = AddIncomeForm(copy_request)
            elif 'editButton' in request.POST.keys():
                writeoffInstance = WriteOff.objects.get(id=request.POST['writeOffId'])
                form = AddExpenseForm(request.POST, instance=writeoffInstance)

            if form.is_valid():
                form.save()
                return redirect('expense_overview')
        return redirect('expense_overview')
    else:
        expenseForm = AddExpenseForm()
        incomeForm = AddIncomeForm()

    context = {
        'totals': totals,
        'writeoffs': writeoffs,
        'expenseForm': expenseForm,
        'incomeForm': incomeForm,
    }

    
    return render(request, 'legacy_lineage/write_offs.html', context)

@login_required
def add_writeoff(request):
    if request.method == 'POST':
        copy_request = request.POST.copy()
        copy_request['user'] = request.user
        form = AddExpenseForm(copy_request)
        if form.is_valid():
            form.save()
            return redirect('expense_overview')
    else:
        form = AddExpenseForm()

    return render(request, 'legacy_lineage/add_write_off.html', {'form': form})

@login_required
def edit_writeoff(request, pk):
    writeoff = get_object_or_404(WriteOff, pk=pk)
    if request.method == 'POST':
        form = AddExpenseForm(request.POST, instance=writeoff)
        if form.is_valid():
            form.save()
            return redirect('expense_overview')
    else:
        form = AddExpenseForm(instance=writeoff)

    return render(request, 'legacy_lineage/edit_write_off.html', {'form': form, 'writeoff': writeoff})

@login_required
def delete_writeoff(request, pk):
    writeoff = get_object_or_404(WriteOff, pk=pk)
    if request.method == 'POST':
        writeoff.delete()
        return redirect('expense_overview')

    return render(request, 'legacy_lineage/delete_write_off.html', {'writeoff': writeoff})

@login_required
def dashboard(request):
    
    # Revenue Data
    total_revenue = Revenue.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    yearly_revenue = Revenue.objects.filter(date__year=2023).aggregate(Sum('amount'))['amount__sum'] or 0

    # Expense Data with Filters
    writeoffs = WriteOff.objects.all()
    expenses_by_category = writeoffs.values('category').annotate(total=Sum('amount'))

    expense_totals = {item['category']: float(item['total']) for item in expenses_by_category}
    print(expense_totals)

    # Recent Transactions (Filtered)
    recent_transactions = writeoffs.order_by('-date')[:5]

    # Yearly Growth Data
    growth_data = Revenue.objects.annotate(year=ExtractYear('date')).values('year').annotate(
        total=Sum('amount')).order_by('year')

    
        
    context = {
        'total_revenue': total_revenue,
        'yearly_revenue': yearly_revenue,
        'expenses': expense_totals,
        'recent_transactions': recent_transactions,
        'growth_data': list(growth_data),  # Convert QuerySet to a list for JavaScript
    }

    return render(request, 'legacy_lineage/admin_dashboard.html', context)

@login_required
def writeoff_detail(request, pk):
    try:
        writeoff = WriteOff.objects.get(pk=pk)
        print(writeoff)
        data = {
            'category': writeoff.category,
            'amount': float(writeoff.amount),
            'description': writeoff.description,
            'date': writeoff.date.strftime('%Y-%m-%d'),
        }
        print(data)
        return JsonResponse(data)
    except WriteOff.DoesNotExist:
        return JsonResponse({'error': 'Write-off not found'}, status=404)

@login_required
def tenant_dashboard(request):
    # Get the currently logged-in tenant
    userProf = UserProfile.objects.get(user=request.user)
    tenant = Tenant.objects.get(userProf=userProf)
    current_balance = payment_charges_totals(tenant)

    # Count active maintenance requests
    active_requests = MaintenanceRequest.objects.filter(tenant=userProf.user, status='Active').count()

    context = {
        'tenant_name': userProf.user.first_name,
        'current_balance': current_balance,
        'active_requests': active_requests,
    }

    return render(request, 'legacy_lineage/tenant_dashboard.html', context)

@login_required
def register_admin(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Do not save yet
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.is_staff = True  # Make the new user an admin
            user.save()  # Save after adding extra fields
            up = UserProfile(
                user=user, business_type="Legacy"
            )
            up.save()
            messages.success(request, 'New admin registered successfully.')
            return redirect('admin_dash')  # Replace with your admin dashboard URL
    else:
        form = UserCreationForm()

    return render(request, 'legacy_lineage/register_admin.html', {'form': form})

@login_required
def maintenance_request(request):
    if request.method == 'POST':
        copy_request = request.POST.copy()
        copy_request['tenant'] = Tenant.objects.get(user=request.user)
        form = MaintenanceRequestForm(copy_request)
        if form.is_valid():
            form.save()
            return redirect('tenant_dashboard')  # Redirect after successful submission
    else:
        form = MaintenanceRequestForm()

    return render(request, 'legacy_lineage/maintenance_request.html', {'form': form})

@login_required
def register_tenant(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Do not save yet
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()  # Save after adding extra fields
            up = UserProfile(
                user=user, business_type="Tenant"
            )
            up.save()
            messages.success(request, 'New tenant registered successfully.')
            return redirect('admin_dash')  # Replace with your admin dashboard URL
    else:
        form = UserCreationForm()

    return render(request, 'legacy_lineage/register_tenant.html', {'form': form})

@login_required
def property_detail(request, pk):
    try:
        property = Property.objects.get(pk=pk)
        print(property)
        data = {
            'address': property.address,
            'city': property.city,
            'state': property.state,
            'zip_code': property.zip_code,
            'lease_start_date': property.lease_start_date.strftime('%Y-%m-%d'),
            'lease_end_date': property.lease_end_date.strftime('%Y-%m-%d'),
            'square_footage': property.square_footage,
            'year_built': property.year_built,
            'notes': property.notes,
            'maintenance_contact': property.maintenance_contact,
            'maintenance_phone': property.maintenance_phone,
            'manager_name': property.manager_name,
        }
        print(data)
        return JsonResponse(data)
    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property not found'}, status=404)
    
def payment_center(request):
    tenant = Tenant.objects.get(userProf__user=request.user)
    current_balance = payment_charges_totals(tenant)
    # stripe_process_fee = ((-current_balance) * Decimal(.029)) + Decimal(.30)
    prepay_amount = current_balance - tenant.monthly_rent
    print(current_balance)
    print(prepay_amount)
    return render(request, "legacy_lineage/make_payment.html",{
        "tenant": tenant,
        "current_balance": -current_balance,
        "prepay_amount": -prepay_amount,
        # 'stripe_process_fee': stripe_process_fee
    })

@login_required
def add_payment_method_page(request):
    return render(request, "legacy_lineage/add_payment.html")

def create_payment_intent(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tenant_id = data['tenant_id']

            # Fetch tenant details
            tenant = Tenant.objects.get(id=tenant_id)
            amount = int(tenant.monthly_rent * 100)  # Convert to cents

            # Create a PaymentIntent for the rent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )

            return JsonResponse({'clientSecret': payment_intent['client_secret']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def save_payment_method(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        # try:
        data = json.loads(request.body)
        payment_method_id = data.get("payment_method_id")
        tenant = Tenant.objects.get(userProf__user=request.user)  # Ensure user is authenticated

        if not payment_method_id or not tenant.stripe_payment_data:
            return JsonResponse({"error": "Invalid request"}, status=400)
        else:
            tenantStripe = tenant.stripe_payment_data

        # Create a Stripe customer if they don't already have one
        if not tenantStripe.stripe_customer_id:
            customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.get_full_name(),
            )
            tenantStripe.stripe_customer_id = customer.id
            tenant.save()

        # Attach payment method to the customer
        stripe.PaymentMethod.attach(
            payment_method_id,
            customer=tenantStripe.stripe_customer_id
        )

        # Set default payment method for future charges
        stripe.Customer.modify(
            tenantStripe.stripe_customer_id,
            invoice_settings={"default_payment_method": payment_method_id}
        )

        # Store the payment method locally in the database
        tenantStripe.stripe_payment_method_id = payment_method_id
        payment_method = stripe.PaymentMethod.retrieve(payment_method_id)

        tenantStripe.last4 = payment_method.card.last4,  # Store last 4 digits for reference
        tenantStripe.brand = payment_method.card.brand
        tenantStripe.save()

        return JsonResponse({"success": True})
        # except Exception as e:
        #     return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Redirect back to Payment Center after adding the payment method
def add_payment_success(request):
    return redirect("payment_center")

def review_payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    tenant = Tenant.objects.get(userProf__user=request.user)
    selected_amount = request.GET.get("amount")  
    selected_method_id = request.GET.get("method")  
    selected_date = request.GET.get("date")  
    print(f"Payment Method: {selected_method_id}")
    # Fetch the correct Payment Method
    try:
        selected_method = PaymentMethod.objects.get(id=selected_method_id, tenant=tenant)
    except PaymentMethod.DoesNotExist:
        messages.error(request, "Invalid payment method selected.")
        return redirect("make_payments")

    # Convert amount selection to actual value
    current_balance = payment_charges_totals(tenant)
    prepay_amount = current_balance - tenant.monthly_rent

    if not selected_amount:
        messages.error(request, "No payment amount selected.")
        return redirect("payment_center")
    else:
        if selected_amount == "full":
            selected_amount = -current_balance
        elif selected_amount == "full-pre":
            selected_amount = -prepay_amount
        else:
            selected_amount = Decimal(selected_amount)

    if request.method == "POST":
        print(f"Processing Payment - Method: {selected_method_id}, Amount: {selected_amount}, Date: {selected_date}")
        payment_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date() if selected_date else date.today()
        if payment_date_obj == date.today():
            # **Process payment immediately**
            try:
                stripe.PaymentIntent.create(
                    amount=int(selected_amount * 100),  # Convert to cents
                    currency="usd",
                    customer=tenant.stripe_payment_data.stripe_customer_id,
                    payment_method=selected_method.stripe_payment_method_id,
                    confirm=True,
                    return_url=request.build_absolute_uri(reverse("payment_success"))
                )
                # Save transaction to database
                Transaction.objects.create(
                    tenant=tenant.userProf,
                    tenantChoice=tenant,
                    transaction_type="Payment",
                    category="Rent",
                    amount=selected_amount,
                    description="Monthly Rent Payment",
                    status="Completed",
                    payment_method=selected_method
                )
                messages.success(request, "Payment was successful!")
                return redirect("make_payments")
            except stripe.error.CardError as e:
                error_message = f"Payment failed: {str(e)}"
                print(error_message)
                print('CHECK 1')
                messages.error(request, f"Card error: {e.user_message}")
            except stripe.error.StripeError as e:
                error_message = f"Payment failed: {str(e)}"
                print(error_message)
                print('CHECK 2')
                messages.error(request, f"Payment failed: {str(e)}")
            except ValueError as e:
                error_message = f"Payment failed: {str(e)}"
                print(error_message)
                print('CHECK 3')
                messages.error(request, str(e))  # Custom validation errors
            except Exception as e:
                error_message = f"Payment failed: {str(e)}"
                print(error_message)
                print('CHECK 4')
                messages.error(request, f"Unexpected error: {str(e)}")
            return redirect("payment_cancel")
        else:
            # **Schedule the payment for the future**
            Transaction.objects.create(
                tenant=tenant,
                transaction_type="Payment",
                amount=selected_amount,
                description="Scheduled Rent Payment",
                category="Rent",
                scheduled_date=payment_date_obj,
                status="Scheduled",
                payment_method=selected_method  # Associate payment method
            )
            messages.success(request, f"Payment has been scheduled for {selected_date}.")
            return redirect("payment_scheduled")

    return render(request, "legacy_lineage/review_payment.html", {
        "tenant": tenant,
        "amount": Decimal(selected_amount),
        "payment_method": selected_method,
        "payment_date": selected_date,
    })

def process_payment(request):
    if request.method == "POST":
        tenant = Tenant.objects.get(userProf__user=request.user)
        amount = request.POST.get("amount")
        payment_method_id = request.POST.get("payment_method_id")
        payment_date = request.POST.get("payment_date")

        try:
            amount_in_cents = int(Decimal(amount) * 100)

            # If the payment is scheduled for the future, store it instead of charging now
            if payment_date and payment_date > str(datetime.today().date()):
                # Store the scheduled payment for later processing
                Transaction.objects.create(
                    tenant=tenant.userProf,
                    tenantChoice=tenant,
                    transaction_type="Payment",
                    description="Scheduled Rent Payment",
                    amount=Decimal(amount),
                    scheduled_date=payment_date,  # Save the future date
                    status="Pending"
                )
                messages.success(request, f"Payment scheduled for {payment_date}.")
                return redirect("payment_success")

            # Charge the card immediately via Stripe
            charge = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency="usd",
                payment_method=payment_method_id,
                confirm=True,
                customer=tenant.stripe_customer_id,
                description="Monthly Rent Payment"
            )

            # Save the successful payment
            Transaction.objects.create(
                tenant=tenant,
                transaction_type="Payment",
                description="Monthly Rent Payment",
                amount=amount,
                status="Completed"
            )

            messages.success(request, "Payment was successful!")
            return redirect("payment_success")

        except stripe.error.CardError as e:
            messages.error(request, f"Payment failed: {e.error.message}")
            return redirect("payment_failed")

    return redirect("make_payment")

def payment_success(request):
    return render(request, "legacy_lineage/payment_success.html")

def payment_cancel(request):
    return render(request, "legacy_lineage/payment_cancel.html")





@csrf_exempt
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = int(data["amount"])  # Ensure it's in cents
            tenant_email = data.get("email", "customer@example.com")

            # Create a Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer_email=tenant_email,
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": "Rent Payment",
                            },
                            "unit_amount": amount,  # Amount in cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url="http://127.0.0.1:8000/payment-success/",
                cancel_url="http://127.0.0.1:8000/payment-cancel/",
            )
            return JsonResponse({"sessionId": session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def get_tenant_payment_info(request, tenant_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        # Fetch tenant details
        tenant = Tenant.objects.get(id=tenant_id)

        # Prepare tenant's payment information
        tenant_info = {
            'name': f'{tenant.userProf.user.first_name} {tenant.userProf.user.last_name}',
            'email': tenant.userProf.user.email,
            'rent_amount': tenant.monthly_rent,  # Example rent amount
            'due_date': tenant.lease_start_date.strftime('%Y-%m-%d'),  # Format due date
        }

        return JsonResponse(tenant_info)

    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)

def setup_autopay(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tenant_id = data['tenant_id']
            payment_method_id = data['payment_method_id']

            # Attach the payment method to the tenant's Stripe customer
            tenant = Tenant.objects.get(id=tenant_id)
            stripe.Customer.modify(
                tenant.stripe_customer_id,
                invoice_settings={"default_payment_method": payment_method_id},
            )

            # Create a subscription for auto-pay
            stripe.Subscription.create(
                customer=tenant.stripe_customer_id,
                items=[{"price": "your_price_id"}],  # Replace with actual price ID
            )

            return JsonResponse({'message': 'Auto-pay enabled'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
