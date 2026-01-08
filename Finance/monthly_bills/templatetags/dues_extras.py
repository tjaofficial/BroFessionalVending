from django import template #type: ignore

register = template.Library()

@register.simple_tag
def dues_cell(grid, member_id, month_date):
    """
    Usage:
      {% dues_cell grid member.id m as cell %}
    Returns:
      {"status": "...", "total": ...} or {"status":"Unpaid","total":0}
    """
    try:
        return grid.get(member_id, {}).get(month_date, {"status": "Unpaid", "total": 0})
    except Exception:
        return {"status": "Unpaid", "total": 0}


@register.filter
def status_class(status):
    s = (status or "").lower()
    if s == "paid":
        return "pill-paid"
    if s == "partial":
        return "pill-partial"
    if s == "unpaid":
        return "pill-unpaid"
    return "pill-na"
