from django import forms #type: ignore

class BackfillRentForm(forms.Form):
    through_month = forms.DateField(
        required=False,
        help_text="Backfill through this month (any day in month is fine). Default: current month."
    )
    include_inactive = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Also include tenants where is_active=False"
    )
