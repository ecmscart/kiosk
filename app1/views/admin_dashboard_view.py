# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache

# Helper function to check if the user is an admin
def is_admin(user):
    return user.is_staff

@login_required  # Ensure the user is logged in
@user_passes_test(is_admin)  # Ensure the user is an admin
@never_cache  # Prevent caching of the dashboard page

def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')



