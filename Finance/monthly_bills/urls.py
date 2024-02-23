from django.urls import path
from . import views

from django.conf import settings
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("FAQ", views.FAQ_page, name="FAQ"),
    path("contact", views.contact_page, name="contact"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("monthly_bills/<str:year>/<str:month>", views.monthly_bills, name="monthly_bills"),
    path("vending/<str:year>/<str:month>", views.vending_finances, name="vendingFinances"),
    path("add_bills", views.add_bills, name="add_bills"),
    path("add_income", views.add_income, name="add_income"),
    path("add_purchase", views.add_purchase, name="add_purchase"),
    path("add_snack", views.add_snack_view, name="add_snack"),
    path("view_snacks", views.view_snacks_view, name="view_snacks"),
    path("add_stock/<str:itemID>", views.add_stock_view, name="add_stock"),
    
    path("vending", views.vending_dashboard, name="vendDash"),
    path("fleet", views.fleet, name="fleet"),
    path("addFleet/<str:selector>", views.add_fleet, name="addFleet"),
    path("inventory/", views.inventory, name="inventory"),
    path("<str:type>/<str:id_tag>", views.machine_options, name="machineDash"),
    path("<str:type>/<str:id_tag>/vmax576", views.vmax576_is, name="vmax576_is"),
    path("<str:type>/<str:id_tag>/vmax576/restock-data", views.vmax576_rd, name="vmax576_rd"),
    path("<str:type>/<str:id_tag>/RS900", views.RS900_is, name="RS900_is"),
    path("<str:type>/<str:id_tag>/GF12_3506_3506A", views.GF12_3506_3506A_is, name="GF12_3506_3506A_is"),
    path("<str:type>/<str:id_tag>/stock", views.stock, name="stock"),
    path("<str:type>/<str:id_tag>/stock/<str:selector>", views.add_item, name="addItem"),
    path("add_gas_log", views.add_gas_log, name="addGas"),
    path("add_mileage_log", views.add_mileage_log, name="addMileage"),
    path("gas_log", views.gas_log, name="gasLog"),
]