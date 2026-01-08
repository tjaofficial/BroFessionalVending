from collections import defaultdict
from datetime import date
from decimal import Decimal
from django.contrib.auth.decorators import login_required #type: ignore
from django.db.models import Sum, Q #type: ignore
from django.db.models.functions import TruncMonth #type: ignore
from django.shortcuts import render, redirect #type: ignore
from django.contrib import messages #type: ignore
from ...models import Transaction, WriteOff, Tenant, UserProfile
from ...utils import first_of_month, add_months
from django.views.decorators.http import require_POST #type: ignore
from django.utils import timezone #type: ignore

@login_required
def rent_overview(request):
    # (Optional) if you have roles, restrict to admins/staff
    # if not request.user.is_staff: return redirect("tenant_dashboard")

    today = date.today()
    current_month = first_of_month(today)

    # --- QUICK ADD PAYMENT (Mom flow) ---
    if request.method == "POST" and "record_payment" in request.POST:
        tenant_id = request.POST.get("tenant_id")
        amount = Decimal(request.POST.get("amount", "0"))
        month_str = request.POST.get("rent_month")  # "2026-01-01"
        note = request.POST.get("note", "").strip()

        rent_month = date.fromisoformat(month_str) if month_str else current_month
        rent_month = first_of_month(rent_month)

        tenant = Tenant.objects.get(id=tenant_id)

        # 1) Tenant ledger
        Transaction.objects.create(
            tenant=tenant.userProf,
            tenantChoice=tenant,
            transaction_type="Payment",
            category="Rent",
            amount=amount,
            description=note or "Rent payment (manual entry)",
            status="Completed",
            rent_month=rent_month,
            payment_method=None,  # cash/check/etc; you can add a simple field later if you want
        )

        # 2) Tax/bookkeeping ledger
        WriteOff.objects.create(
            category="rent",
            amount=amount,
            description=f"Rent received - {tenant.userProf.user.get_full_name()} ({rent_month.strftime('%b %Y')})",
            date=today,
            transaction_type="Income",
            added_by=UserProfile.objects.get(user=request.user),
        )

        messages.success(request, f"Recorded ${amount} for {tenant.userProf.user.get_full_name()} ({rent_month.strftime('%b %Y')}).")
        return redirect("rent_overview")

    # --- BUILD LEDGER ROWS ---
    rent_qs = (
        Transaction.objects
        .filter(category="Rent", rent_month__isnull=False)
        .values("tenantChoice_id", "tenant__user__first_name", "tenant__user__last_name", "rent_month")
        .annotate(
            due=Sum("amount", filter=Q(transaction_type="Charge")) ,
            paid=Sum("amount", filter=Q(transaction_type="Payment")) ,
        )
        .order_by("tenant__user__last_name", "tenant__user__first_name", "rent_month")
    )

    ledger_rows = []
    past_due_map = defaultdict(lambda: {"name": "", "months": [], "total_due": Decimal("0.00")})

    for r in rent_qs:
        due = r["due"] or Decimal("0.00")
        paid = r["paid"] or Decimal("0.00")
        balance = due - paid  # >0 means still owed

        if due == 0 and paid != 0:
            # odd case: payment with no charge; still show if you want
            pass

        if balance <= 0:
            status = "Paid"
        elif paid == 0:
            status = "Unpaid"
        else:
            status = "Partial"

        tenant_id = r["tenantChoice_id"]
        tenant_name = f'{r["tenant__user__first_name"]} {r["tenant__user__last_name"]}'.strip()
        month_label = r["rent_month"].strftime("%b %Y")

        ledger_rows.append({
            "tenant_id": tenant_id,
            "tenant_name": tenant_name,
            "rent_month": r["rent_month"],
            "month_label": month_label,
            "due": due,
            "paid": paid,
            "balance": balance,
            "status": status,
        })

        if balance > 0:
            past_due_map[tenant_id]["name"] = tenant_name
            past_due_map[tenant_id]["months"].append(month_label)
            past_due_map[tenant_id]["total_due"] += balance

    past_due_list = []
    for tenant_id, info in past_due_map.items():
        past_due_list.append({
            "tenant_id": tenant_id,
            "tenant_name": info["name"],
            "months": info["months"],
            "total_due": info["total_due"],
        })
    past_due_list.sort(key=lambda x: x["total_due"], reverse=True)

    tenants = Tenant.objects.all().select_related("userProf__user").order_by("userProf__user__last_name")

    context = {
        "past_due_list": past_due_list,
        "ledger_rows": ledger_rows,
        "tenants": tenants,
        "current_month": current_month,
    }
    return render(request, "legacy_lineage/rent_overview.html", context)

def backfill_rent_for_tenant(*, tenant: Tenant, through_month: date) -> int:
    """
    Create missing monthly rent Charge transactions from lease_start month
    through `through_month` (inclusive). Idempotent.
    Returns number created.
    """
    if not tenant.userProf:
        return 0

    start_month = first_of_month(tenant.lease_start_date)
    end_month = first_of_month(through_month)

    # Don’t backfill “before” the lease starts
    if end_month < start_month:
        return 0

    # OPTIONAL: if you want to stop at lease_end_date month, uncomment:
    # lease_end_month = first_of_month(tenant.lease_end_date)
    # end_month = min(end_month, lease_end_month)

    # Pull existing rent charges once
    existing = set(
        Transaction.objects.filter(
            tenantChoice=tenant,
            transaction_type="Charge",
            category="Rent",
            rent_month__gte=start_month,
            rent_month__lte=end_month,
        ).values_list("rent_month", flat=True)
    )

    created = 0
    m = start_month
    while m <= end_month:
        if m not in existing:
            Transaction.objects.create(
                tenant=tenant.userProf,
                tenantChoice=tenant,
                transaction_type="Charge",
                category="Rent",
                amount=Decimal(tenant.monthly_rent),
                description=f"Monthly rent charge ({m.strftime('%B %Y')})",
                status="Completed",
                rent_month=m,
            )
            created += 1
        m = add_months(m, 1)

    return created

@require_POST
@login_required
def backfill_rent_charges(request):
    today = timezone.localdate()
    through_month = first_of_month(today)

    tenants = Tenant.objects.filter(is_active=True).select_related("userProf", "userProf__user")

    total_created = 0
    for tenant in tenants:
        total_created += backfill_rent_for_tenant(tenant=tenant, through_month=through_month)

    messages.success(
        request,
        f"Backfill complete through {through_month.strftime('%Y-%m')}. Created {total_created} rent charge(s)."
    )

    return redirect("rent_overview")  # <-- use your rent page url name

