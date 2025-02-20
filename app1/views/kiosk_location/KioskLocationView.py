from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app1.models import KioskLocations
from django.utils.timezone import now


@login_required
def kiosk_location_list(request):
    locations = KioskLocations.objects.all()
    return render(request, 'admin/kiosk_location/kiosk_location.html',{'locations': locations})

@login_required
def location_ajax_list(request):
    draw = int(request.GET.get('draw', 1))  # Draw counter to keep track of DataTable requests
    start = int(request.GET.get('start', 0))  # The starting point of the data (pagination)
    length = int(request.GET.get('length', 10))  # The number of records per page
    search_value = request.GET.get('search[value]', '').strip()  # Search keyword

    locations = KioskLocations.objects.all()
    if search_value:
        locations = locations.filter(name__icontains=search_value)

    order_column = int(request.GET.get('order[0][column]', 0))  # Column index for sorting
    print(order_column) 
    order_dir = request.GET.get('order[0][dir]', 'DESC')
    if order_column == 0:
        locations = locations.order_by('-id')

    locations_paginated = locations[start:start+length]
    data = [
        {    'location_id': location.id,
            'name': location.name,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'status': location.status,
            'created_at': location.created_at.strftime('%b. %d, %Y, %I:%M %p') if location.created_at else "N/A",  # Handle None
        }
        for location in locations_paginated
    ]
    records_total = KioskLocations.objects.count()  # Total number of locations in the database
    records_filtered = locations.count()
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
def create_location(request):
    if request.is_ajax():
        try:
            # Parse POST data
            name = request.POST.get('name')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            status = request.POST.get('status')

            # Validate inputs
            if not name or not latitude or not longitude or status not in ['0', '1']:
                return JsonResponse({'error': 'Invalid input data'}, status=400)

            # Create the location
            location = KioskLocations.objects.create(
                name=name,
                latitude=latitude,
                longitude=longitude,
                status=status,
                created_at=now()  # Set the current timestamp
            )

            # Respond with the newly created location's data
            return JsonResponse({
                'message': 'Location created successfully',
                'location': {
                    'location_id': location.id,
                    'name': location.name,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'status': location.status,
                    'created_at': location.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# API for deleting a location (AJAX)
@login_required
def delete_location(request, location_id):
    if request.is_ajax():
        location = KioskLocations.objects.get(id=location_id)
        location.delete()
        return JsonResponse({'message': 'Location deleted successfully'})
    
# API for editing a location (AJAX)
@login_required
def edit_location(request, location_id):
    location = get_object_or_404(KioskLocations, id=location_id)
    
    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        status = request.POST.get('status')
        
        # Update the location fields
        location.name = name
        location.latitude = latitude
        location.longitude = longitude
        location.status = status

        # Save the updated location
        location.save()

        # Return the updated location details in the response
        return JsonResponse({
            'message': 'Location updated successfully',
            'loaction': {
                'location_id': location.id,
                'name': location.name,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'status': location.status,
                'created_at': location.created_at.strftime('%b. %d, %Y, %I:%M %p')
                
            }
        })
    

def locationList(request):
    if request.method == 'GET':
        # Fetch all active locations, ordered by descending ID
        locations = list(KioskLocations.objects.filter(status=1).order_by('-id').values())
        
        if locations:
            locations_data = {
                'status': True,
                'message': 'success',
                'data': locations
            }
        else:
            locations_data = {
                'status': False,
                'message': 'No locations found',
                'data': []
            }
        
        return JsonResponse(locations_data)


