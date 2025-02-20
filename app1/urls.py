from django.urls import path
from django.contrib.auth import views as auth_views
from app1.views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('kiosklocation/', kiosk_location_list, name='kiosk_location_list'),  # Display all locations
    path('kiosklocation/location_ajax_list', location_ajax_list, name='location_ajax_list'),
    path('kiosklocation/create/', create_location, name='create_location'),  # API to create location
    path('kiosklocation/edit/<int:location_id>/', edit_location, name='edit_location'),  # API to edit location
    path('kiosklocation/delete/<int:location_id>/', delete_location, name='delete_location'),  # API to delete location

    path('kioskprint/', kiosk_printer_list, name='kiosk_printer_list'),  # Display all prints
    path('kioskprint/display_printer', display_printer, name='display_printer'),
    path('kioskprint/delete/<int:id>/', delete_printer, name='delete_printer'),  # API to delete prints
    path('kioskprint/create/', create_printer, name='create_printer'),  # API to create prints
    path('kioskprint/edit/<int:id>/', edit_printer, name='edit_printer'),  # API to edit prints

    path('printcost/', price_cost_list, name='price_cost_list'),  # Display costs
    path('printcost/display_cost', display_cost, name='display_cost'),
    path('printcost/delete/<int:id>/', delete_cost, name='delete_cost'),  # API to delete costs
    path('printcost/create/', create_cost, name='create_cost'),  # API to create costs
    path('printcost/edit/<int:id>/', edit_cost, name='edit_cost'),  # API to edit costs

    path('orders/', order_list, name='order_list'),
    path('orders/display/', display_order, name='display_order'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('orders/<int:order_id>/update_status/', edit_order_status, name='edit_order_status'),

]

