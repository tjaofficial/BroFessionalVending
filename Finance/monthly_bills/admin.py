from django.contrib import admin, messages #type: ignore
from .models import *
from .views.legacy_lineage.admin_forms import BackfillRentForm
from .utils import first_of_month
from django.shortcuts import redirect, render #type: ignore
from django.urls import path #type: ignore
from .views.legacy_lineage.rent_view import backfill_rent_for_tenant

# Register your models here.
admin.site.register(bill_items_model)
admin.site.register(bills_model)
admin.site.register(pay_log)
admin.site.register(income_log)
admin.site.register(purchase_model)
admin.site.register(fleet_model)
admin.site.register(machine_stock_model)
admin.site.register(vmax576_model)
admin.site.register(machine_database_model)
admin.site.register(gas_log_model)
admin.site.register(mileage_log_model)
admin.site.register(RS900_model)
admin.site.register(inventory_sheets_model)
admin.site.register(vending_finance)
admin.site.register(price_model)
admin.site.register(cantaLogs_model)
admin.site.register(FAQ_model)
admin.site.register(item_data_model)
admin.site.register(item_stock_model)
admin.site.register(machine_model_model)
admin.site.register(machine_build_model)
admin.site.register(canta_payments_model)
# admin.site.register(Tenant)
admin.site.register(Property)
admin.site.register(WriteOff)
admin.site.register(Revenue)
admin.site.register(MaintenanceRequest)
admin.site.register(Transaction)
admin.site.register(UserProfile)
admin.site.register(home_inventory_model)
admin.site.register(LossStockModel)
admin.site.register(PaymentMethod)
admin.site.register(LLCMember)
admin.site.register(MemberDuesPayment)

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("id", "userProf", "property", "unit_number", "monthly_rent", "lease_start_date", "is_active")
    list_filter = ("is_active", "property")
    search_fields = ("userProf__user__username", "userProf__user__first_name", "userProf__user__last_name")

    actions = ["backfill_rent_charges_action"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "backfill-rent/",
                self.admin_site.admin_view(self.backfill_rent_view),
                name="monthly_bills_tenant_backfill_rent",
            ),
        ]
        return custom_urls + urls

    def backfill_rent_charges_action(self, request, queryset):
        """
        Quick action: backfills selected tenants through current month.
        """
        today = timezone.localdate()
        through_month = first_of_month(today)

        total_created = 0
        for tenant in queryset:
            total_created += backfill_rent_for_tenant(tenant=tenant, through_month=through_month)

        messages.success(request, f"Backfill complete. Created {total_created} rent charge(s).")
    backfill_rent_charges_action.short_description = "Backfill rent charges (through current month)"

    def backfill_rent_view(self, request):
        """
        Nice UI view: pick through_month + include_inactive, and apply to ALL tenants.
        """
        if request.method == "POST":
            form = BackfillRentForm(request.POST)
            if form.is_valid():
                through = form.cleaned_data.get("through_month") or timezone.localdate()
                include_inactive = form.cleaned_data.get("include_inactive") or False

                tenants = Tenant.objects.all()
                if not include_inactive:
                    tenants = tenants.filter(is_active=True)

                total_created = 0
                through_month = first_of_month(through)

                for tenant in tenants:
                    total_created += backfill_rent_for_tenant(tenant=tenant, through_month=through_month)

                messages.success(request, f"Backfill complete through {through_month.strftime('%Y-%m')}. Created {total_created} rent charge(s).")
                return redirect("..")
        else:
            form = BackfillRentForm()

        context = dict(
            self.admin_site.each_context(request),
            title="Backfill Rent Charges",
            form=form,
        )
        return render(request, "admin/monthly_bills/tenant/backfill_rent.html", context)

