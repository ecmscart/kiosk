from django.urls import path
from django.contrib.auth import views as auth_views
from app1.views import *

urlpatterns = [
   path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('KioskLocation/', kiosk_location_list, name='kiosk_location_list'),  # Display all products
    path('KioskLocation/location_ajax_list', location_ajax_list, name='location_ajax_list'),
    path('KioskLocation/create/', create_location, name='create_location'),  # API to create category
    path('KioskLocation/edit/<int:location_id>/', edit_location, name='edit_location'),  # API to edit category
    path('KioskLocation/delete/<int:location_id>/', delete_location, name='delete_location'),  # API to delete category
]