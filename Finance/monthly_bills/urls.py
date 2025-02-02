from django.urls import path
from . import views

from django.conf import settings
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("FAQ", views.FAQ_page, name="FAQ"),
    path("contact", views.contact_page, name="contact"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("monthly_bills/<str:year>/<str:month>", views.monthly_bills, name="monthly_bills"),
    path("vending/<str:year>/<str:month>", views.vending_finances, name="vendingFinances"),
    path("add_bills", views.add_bills, name="add_bills"),
    path("add_income", views.add_income, name="add_income"),
    path("add_purchase", views.add_purchase, name="add_purchase"),
    path("add_snack", views.add_snack_view, name="add_snack"),
    path("view_snacks", views.view_snacks_view, name="view_snacks"),
    path("add_stock/<str:itemID>", views.add_stock_view, name="add_stock"),
    path("<str:machineID>/build", views.machine_build_view, name="machine_build"),
    path("view_snacks/item/<str:itemID>", views.view_individual_snack_view, name="view_individual_snack"),
    path("api/get-statistics/", views.get_statistics, name="get-statistics"),


    path("vending", views.vending_dashboard, name="vendDash"),
    path("fleet", views.fleet, name="fleet"),
    path("addFleet/<str:selector>", views.add_fleet, name="addFleet"),
    path("inventory/", views.inventory, name="inventory"),
    path("machine/<str:type>/<str:id_tag>", views.machine_options, name="machineDash"),
    path("<str:type>/<str:id_tag>/vmax576", views.vmax576_is, name="vmax576_is"),
    path("<str:type>/<str:id_tag>/vmax576/restock-data", views.vmax576_rd, name="vmax576_rd"),
    path("<str:type>/<str:id_tag>/RS900", views.RS900_is, name="RS900_is"),
    path("<str:type>/<str:id_tag>/stock", views.stock, name="stock"),
    path("<str:type>/<str:id_tag>/stock/<str:selector>", views.add_item, name="addItem"),
    path("add_gas_log", views.add_gas_log, name="addGas"),
    path("add_mileage_log", views.add_mileage_log, name="addMileage"),
    path("gas_log", views.gas_log, name="gasLog"),

    path("<str:type>/<str:id_tag>/inventory-sheet/<str:buildID>", views.universal_is, name="inventorySheet"),
    path("<str:type>/<str:id_tag>/archive/<str:date>", views.view_is, name="viewInventory"),
    path("<str:type>/<str:id_tag>/canta-payments", views.canta_payments, name="cantaPayments"),
    
    path("<str:type>/<str:id_tag>/analytics", views.analytics_page, name="analyticsDash"),

    #Legacy Lineage
    path("legacyportal/add_tenant", views.add_tenant, name="add_tenant"),
    path("legacyportal/add_property", views.add_property, name="add_property"),
    path("legacyportal/view_properties", views.view_properties, name="view_properties"),
    path("legacyportal/view_tenants", views.view_tenants, name="view_tenants"),
    path('legacyportal/expense_overview', views.expense_overview, name='expense_overview'),
    path('legacyportal/expense_overview/add/', views.add_writeoff, name='add_writeoff'),
    path('legacyportal/expense_overview/edit/<int:pk>/', views.edit_writeoff, name='edit_writeoff'),
    path('legacyportal/expense_overview/delete/<int:pk>/', views.delete_writeoff, name='delete_writeoff'),
    path('legacyportal/admin_dash', views.dashboard, name='admin_dash'),
    path('api/writeoff/<int:pk>/', views.writeoff_detail, name='writeoff_detail'),
    path('api/property/<int:pk>/', views.property_detail, name='property_detail'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('legacyportal/register-admin/', views.register_admin, name='register_admin'),
    path('legacyportal/register-tenant/', views.register_tenant, name='register_tenant'),
    path('tenant/maintenance-request/', views.maintenance_request, name='maintenance_request'),
    path('tenant/make-payments/', views.payment_center, name='make_payments'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('get-tenant-payment-info/<int:tenant_id>/', views.get_tenant_payment_info, name='get_tenant_payment_info'),

]