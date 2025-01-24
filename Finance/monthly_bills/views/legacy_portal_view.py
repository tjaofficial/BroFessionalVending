from django.shortcuts import render, redirect, get_object_or_404
from ..forms import TenantForm, PropertyForm, AddExpenseForm, MaintenanceRequestForm, AddIncomeForm
from ..models import Property, Tenant, WriteOff, Revenue, MaintenanceRequest, Transaction, UserProfile
from django.db.models import Sum
from django.db.models.functions import ExtractYear, Upper
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
import stripe
from django.conf import settings
import json



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
        'auto': WriteOff.objects.filter(category='auto').aggregate(Sum('amount'))['amount__sum'] or 0,
        'business': WriteOff.objects.filter(category='business').aggregate(Sum('amount'))['amount__sum'] or 0,
        'home_office': WriteOff.objects.filter(category='home_office').aggregate(Sum('amount'))['amount__sum'] or 0,
        'meals': WriteOff.objects.filter(category='meals').aggregate(Sum('amount'))['amount__sum'] or 0,
        'property': WriteOff.objects.filter(category='property').aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    writeoffs = WriteOff.objects.all().order_by('-date')
    for x in writeoffs:
        x.added_by = UserProfile.objects.get(user=request.user)
        x.save()

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
    tenant = UserProfile.objects.get(user=request.user)
    transactionQuery = Transaction.objects.filter(tenant=tenant)
    total_charges = 1650.00
    total_payments = 825.00
    for trans in transactionQuery:
        if trans.transaction_type == 'charge':
            total_charges += float(trans.amount)
        else:
            total_payments += float(trans.amount)
    current_balance = total_payments - total_charges
    
    # Calculate the current balance (total charges - total payments)
    #total_charges = tenant.charges.aggregate(total=models.Sum('amount'))['total'] or 0
    #total_payments = Transaction.objects.filter(tenant=tenant).aggregate(total=models.Sum('amount'))['total'] or 0

    # Count active maintenance requests
    active_requests = MaintenanceRequest.objects.filter(tenant=tenant.user, status='Active').count()

    context = {
        'tenant_name': tenant.user.first_name,
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

def payment_center(request):

    return render(request, "legacy_lineage/make_payment.html",{

    })

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
