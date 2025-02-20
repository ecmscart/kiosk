from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app1.models import *
from django.utils.timezone import now
from django.db.models import OuterRef, Subquery

@login_required
def kiosk_printer_list(request):
    printers = KioskPrinter.objects.all()
    locations = KioskLocations.objects.filter(status=1).values('id','name') 
    return render(request, 'admin/kiosk_print/kiosk_print.html', {
        'printers': printers,
        'locations': locations
    })


@login_required
def display_printer(request):
    draw = int(request.GET.get('draw', 1))  # Draw counter to keep track of DataTable requests
    start = int(request.GET.get('start', 0))  # The starting point of the data (pagination)
    length = int(request.GET.get('length', 10))  # The number of records per page
    search_value = request.GET.get('search[value]', '').strip()  # Search keyword

    printers = KioskPrinter.objects.all()
    if search_value:
        printers = printers.filter(name__icontains=search_value)

    order_column = int(request.GET.get('order[0][column]', 0))  # Column index for sorting
    order_dir = request.GET.get('order[0][dir]', 'DESC')
    if order_column == 0:
        printers = printers.order_by('-id')

    printers_paginated = printers[start:start+length]
    data = [
        {    'id': printer.id,
            'location_id': printer.location_id,
            'printer_no': printer.printer_no,
            'name': printer.name,
            'A3tray':printer.A3tray,
            'status': printer.status,
            'created_at': printer.created_at.strftime('%b. %d, %Y, %I:%M %p') if printer.created_at else "N/A",  # Handle None
        }
        for printer in printers_paginated
    ]
    records_total = KioskPrinter.objects.count()  # Total number of locations in the database
    records_filtered = printers.count()
    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'draw': draw,
    })


# API for creating a location (AJAX)
@login_required
def create_printer(request):
    if request.is_ajax():
        try:
            # Parse POST data
            location_id = request.POST.get('location_id')
            printer_no = request.POST.get('printer_no')
            name = request.POST.get('name')
            A3tray=request.POST.get('A3tray')
            status = request.POST.get('status')
           
            # Validate inputs
            if not location_id or not printer_no or not name:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            # Create the location
            printer = KioskPrinter.objects.create(
            location_id = location_id,
            printer_no = printer_no,
            name = name,
            A3tray=A3tray,
            status =status,
            created_at=now()  # Set the current timestamp
            )

            # Respond with the newly created location's data
            return JsonResponse({
                'message': 'Printer created successfully',
                'printer': {
                    'id': printer.id,
                    'location_id': printer.location_id,
                    'printer_no': printer.printer_no,
                    'name': printer.name,
                    'A3tray': printer.A3tray,
                    'status': printer.status,
                    'created_at': printer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# API for deleting a printers (AJAX)
@login_required
def delete_printer(request,id):
    if request.is_ajax():
        printer = KioskPrinter.objects.get(id=id)
        printer.delete()
        return JsonResponse({'message': 'Printer deleted successfully'})
    
# API for editing a location (AJAX)
@login_required
def edit_printer(request, id):
    printer = get_object_or_404(KioskPrinter, id=id)
    
    if request.method == 'POST' and request.is_ajax():
        location_id = request.POST.get('location_id')
        printer_no = request.POST.get('printer_no')
        name = request.POST.get('name')
        A3tray= request.POST.get('A3tray')
        status = request.POST.get('status')
        
        
        # Update the location fields
        printer.location_id = location_id
        printer.printer_no = printer_no
        printer.name = name
        printer.A3tray=A3tray
        printer.status = status
        

        # Save the updated location
        printer.save()

        # Return the updated location details in the response
        return JsonResponse({
            'message': 'Location updated successfully',
            'printer': {
                'id': printer.id,
                'location_id': printer.location_id,
                'printer_no': printer.printer_no,
                'name': printer.name,
                'A3tray': printer.A3tray,
                'status':printer.status,
                'created_at': printer.created_at.strftime('%b. %d, %Y, %I:%M %p')
                
            }
        })
    

def printerList(request):
   if request.method == 'GET':
        # Subquery to fetch location name based on location_id
        location_subquery = KioskLocations.objects.filter(id=OuterRef('location_id')).values('name')[:1]

        # Fetch printers and add location name
        printers = KioskPrinter.objects.annotate(location_name=Subquery(location_subquery)).order_by('-id').values()

        if printers:
            printers_data = {
                'status': True,
                'message': 'success',
                'data': list(printers)
            }
        else:
            printers_data = {
                'status': False,
                'message': 'No printers found',
                'data': []
            }

        return JsonResponse(printers_data, safe=False)