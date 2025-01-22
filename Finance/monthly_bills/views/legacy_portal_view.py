from django.shortcuts import render, redirect, get_object_or_404
from ..forms import TenantForm, PropertyForm, WriteOffForm, MaintenanceRequestForm
from ..models import Property, Tenant, WriteOff, Revenue, MaintenanceRequest, Transaction, UserProfile
from django.db.models import Sum
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

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

    if request.method == 'POST':
        copy_request = request.POST.copy()
        copy_request['user'] = request.user
        if 'deleteButton' in request.POST.keys():
            writeoffInstance = WriteOff.objects.get(id=request.POST['writeOffId'])
            writeoffInstance.delete()
        else:
            if 'addButton' in request.POST.keys():
                form = WriteOffForm(copy_request)
            elif 'editButton' in request.POST.keys():
                writeoffInstance = WriteOff.objects.get(id=request.POST['writeOffId'])
                form = WriteOffForm(request.POST, instance=writeoffInstance)

            if form.is_valid():
                form.save()
                return redirect('expense_overview')
        return redirect('expense_overview')
    else:
        writeOffForm = WriteOffForm()
        print('hello')

    context = {
        'totals': totals,
        'writeoffs': writeoffs,
        'writeOffForm': writeOffForm,
    }

    
    return render(request, 'legacy_lineage/write_offs.html', context)

@login_required
def add_writeoff(request):
    if request.method == 'POST':
        copy_request = request.POST.copy()
        copy_request['user'] = request.user
        form = WriteOffForm(copy_request)
        if form.is_valid():
            form.save()
            return redirect('expense_overview')
    else:
        form = WriteOffForm()

    return render(request, 'legacy_lineage/add_write_off.html', {'form': form})

@login_required
def edit_writeoff(request, pk):
    writeoff = get_object_or_404(WriteOff, pk=pk)
    if request.method == 'POST':
        form = WriteOffForm(request.POST, instance=writeoff)
        if form.is_valid():
            form.save()
            return redirect('expense_overview')
    else:
        form = WriteOffForm(instance=writeoff)

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
    # Handle search filters
    search_description = request.GET.get('description', '').strip()
    search_category = request.GET.get('category', '').strip()
    date_start = request.GET.get('date_start', None)
    date_end = request.GET.get('date_end', None)

    # Revenue Data
    total_revenue = Revenue.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    yearly_revenue = Revenue.objects.filter(date__year=2023).aggregate(Sum('amount'))['amount__sum'] or 0

    # Expense Data with Filters
    writeoffs = WriteOff.objects.all()

    if search_description:
        writeoffs = writeoffs.filter(description__icontains=search_description)
    if search_category:
        writeoffs = writeoffs.filter(category=search_category)
    if date_start:
        writeoffs = writeoffs.filter(date__gte=date_start)
    if date_end:
        writeoffs = writeoffs.filter(date__lte=date_end)

    expenses_by_category = writeoffs.values('category').annotate(total=Sum('amount'))
    expense_totals = {item['category']: item['total'] for item in expenses_by_category}

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
        'search_description': search_description,
        'search_category': search_category,
        'date_start': date_start,
        'date_end': date_end,
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
    tenant = User.objects.get(id=request.user.id)
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
    active_requests = MaintenanceRequest.objects.filter(tenant=tenant, status='Active').count()

    context = {
        'tenant_name': tenant.first_name,
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
                user=user
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