from datetime import date
from collections import defaultdict
from django.contrib.auth.decorators import login_required #type: ignore
from django.db.models import Sum #type: ignore
from django.shortcuts import render, redirect #type: ignore
from django.utils import timezone #type: ignore
from django.views.decorators.http import require_POST #type: ignore
from monthly_bills.models import LLCMember, MemberDuesPayment, WriteOff, UserProfile
from ...forms import MemberDuesPaymentForm 
from ...utils import first_of_month, month_list_for_year
from django.db import transaction as db_transaction #type: ignore

@login_required
def dues_overview(request):
    year = int(request.GET.get("year", timezone.localdate().year))
    months = month_list_for_year(year)

    members = LLCMember.objects.filter(is_active=True).order_by("display_name")

    # Get all payments for that year (bucketed by dues_month)
    payments_qs = (
        MemberDuesPayment.objects
        .filter(dues_month__year=year)
        .values("member_id", "dues_month")
        .annotate(total=Sum("amount"))
    )

    paid_totals = {(p["member_id"], p["dues_month"]): (p["total"] or 0) for p in payments_qs}

    # Build status grid: member -> month -> status
    # status based on total vs member.monthly_dues
    grid = defaultdict(dict)
    for member in members:
        start_month = first_of_month(member.start_date)

        for m in months:
            if m < start_month:
                grid[member.id][m] = {"status": "N/A", "total": 0}
                continue

            total = paid_totals.get((member.id, m), 0)
            dues = member.monthly_dues

            if total <= 0:
                status = "Unpaid"
            elif total < dues:
                status = "Partial"
            else:
                status = "Paid"

            grid[member.id][m] = {"status": status, "total": total}

    # Payment table (latest first)
    payments_table = (
        MemberDuesPayment.objects
        .select_related("member")
        .filter(dues_month__year=year)
        .order_by("-paid_date", "-created_at")
    )

    form = MemberDuesPaymentForm()

    return render(request, "legacy_lineage/dues_overview.html", {
        "year": year,
        "months": months,
        "members": members,
        "grid": grid,
        "payments": payments_table,
        "form": form,
    })


@require_POST
@login_required
def record_dues_payment(request):
    print(request.POST['apply_month'])
    print("FORM CLASS:", MemberDuesPaymentForm)
    print("FORM FIELDS:", list(MemberDuesPaymentForm.base_fields.keys()))

    form = MemberDuesPaymentForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return redirect("dues_overview")

    with db_transaction.atomic():
        payment = form.save(commit=False)
        payment.save()

        added_by = None
        try:
          added_by = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
          pass

        WriteOff.objects.create(
            category="dues",
            amount=payment.amount,
            description=(
                f"LLC Dues - {payment.member.display_name} "
                f"({payment.dues_month.strftime('%Y-%m')})"
                + (f" | {payment.note}" if payment.note else "")
            ),
            date=payment.paid_date,
            transaction_type="Income",
            added_by=added_by
        )

    return redirect("dues_overview")
