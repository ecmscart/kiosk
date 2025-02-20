import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app1.models import Order
from django.contrib.auth.decorators import login_required

@csrf_exempt  # Disable CSRF for simplicity (consider using CSRF tokens in production)
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON request body
            
            # Extract fields from the request
            total_paid = data.get('total_paid')
            pages_selected = data.get('pages_selected')
            is_singleside = data.get('is_singleside')
            is_color = data.get('is_color')
            no_copy = data.get('no_copy')
            page_type = data.get('page_type')
            date_paid = data.get('date_paid')
            is_paid = data.get('is_paid')
            trx_id = data.get('trx_id')
            mobile_device_id = data.get('mobile_device_id')
            file_name=data.get('file_name')
            order_status = data.get('order_status')

            # Validate required field `page_type`
            if not page_type or page_type not in ['A3', 'A4']:
                return JsonResponse({'status': False, 'message': 'Invalid page type'}, status=400)

            # Create an Order object and save it to the database
            order = Order.objects.create(
                total_paid=total_paid,
                pages_selected=pages_selected,
                is_singleside=is_singleside,
                is_color=is_color,
                no_copy=no_copy,
                page_type=page_type,
                date_paid=date_paid,
                is_paid=is_paid,
                trx_id=trx_id,
                mobile_device_id=mobile_device_id,
                file_name=file_name,
                order_status=order_status
            )

            # Return success response
            return JsonResponse({
                'status': True,
                'message': 'Order created successfully',
                'data': {
                    'total_paid': str(order.total_paid),
                    'pages_selected': order.pages_selected,
                    'is_singleside': order.is_singleside,
                    'is_color': order.is_color,
                    'no_copy': order.no_copy,
                    'page_type': order.page_type,
                    'date_paid' : order.date_paid,
                    'is_paid': order.is_paid,
                    'trx_id': order.trx_id,
                    'mobile_device_id': order.mobile_device_id,
                    'file_name': order.file_name,
                    'order_status': order_status,
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': False, 'message': 'Invalid JSON format'}, status=400)

    return JsonResponse({'status': False, 'message': 'Method Not Allowed'}, status=405)


@login_required
def display_order(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '').strip()

    orders = Order.objects.all()
    if search_value:
        orders = orders.filter(kiosk_location_name__icontains=search_value)

    order_column = int(request.GET.get('order[0][column]', 0))
    if order_column == 0:
        orders = orders.order_by('-order_id')

    orders_paginated = orders[start:start+length]
    data = [
        {
            'order_id': order.order_id,
            'total_paid': order.total_paid,
            'pages_selected': order.pages_selected,
            'is_singleside': order.is_singleside,
            'is_color': order.is_color,
            'no_copy': order.no_copy,
            'page_type': order.page_type,
            'recipt_file': order.recipt_file if order.recipt_file else "N/A",
            'date_paid': order.date_paid.strftime('%b. %d, %Y, %I:%M %p') if order.date_paid else "N/A",
            'date_printed': order.date_printed.strftime('%b. %d, %Y, %I:%M %p') if order.date_printed else "N/A",
            'is_paid': order.is_paid,
            'trx_id': order.trx_id if order.trx_id else "N/A",
            'kiosk_location_name': order.kiosk_location_name,
            'printer_name': order.printer_name,
            'printer_id': order.printer_id,
            'kiosk_id': order.kiosk_id if order.kiosk_id else "N/A",
            'mobile_device_id': order.mobile_device_id if order.mobile_device_id else "N/A",
            'file_name':order.file_name,
            'order_status': order.order_status,
            'created_at': order.created_at.strftime('%b. %d, %Y, %I:%M %p') if order.created_at else "N/A",
        }
        for order in orders_paginated
    ]
    records_total = Order.objects.count()
    records_filtered = orders.count()

    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'draw': draw,
    })


@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'admin/order/order.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'admin/order/order_detail.html', {'order': order})

# API for editing a location (AJAX)
@login_required
def edit_order_status(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    if request.method == 'POST' and request.is_ajax():
        order_status = request.POST.get('order_status')
       
        
        # Update the location fields
        order.order_status = order_status
        

        # Save the updated location
        order.save()

        # Return the updated location details in the response
        return JsonResponse({
            'message': 'Status updated successfully',
            'order': {
                'order_id': order.order_id,
                 'order_status': order.order_status
                
            }
        })
    

def orderlist(request):
    
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '').strip()

    orders = Order.objects.all()
    if search_value:
        orders = orders.filter(kiosk_location_name__icontains=search_value)

   
    orders = orders.order_by('-order_id')

    orders_paginated = orders[start:start+length]
    data = [
        {
            'order_id': order.order_id,
            'total_paid': order.total_paid,
            'pages_selected': order.pages_selected,
            'is_singleside': order.is_singleside,
            'is_color': order.is_color,
            'no_copy': order.no_copy,
            'page_type': order.page_type,
            'recipt_file': order.recipt_file if order.recipt_file else "N/A",
            'date_paid': order.date_paid.strftime('%b. %d, %Y, %I:%M %p') if order.date_paid else "N/A",
            'date_printed': order.date_printed.strftime('%b. %d, %Y, %I:%M %p') if order.date_printed else "N/A",
            'is_paid': order.is_paid,
            'trx_id': order.trx_id if order.trx_id else "N/A",
            'kiosk_location_name': order.kiosk_location_name,
            'printer_name': order.printer_name,
            'printer_id': order.printer_id,
            'kiosk_id': order.kiosk_id if order.kiosk_id else "N/A",
            'mobile_device_id': order.mobile_device_id if order.mobile_device_id else "N/A",
            'file_name':order.file_name,
            'order_status': order.order_status,
            'created_at': order.created_at.strftime('%b. %d, %Y, %I:%M %p') if order.created_at else "N/A",
        }
        for order in orders_paginated
    ]
  

    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data
    })

def orderbyid(request):
    order_id = request.GET.get('order_id')

    if order_id:
        order = Order.objects.filter(order_id=order_id).first()  # Get a single order or None
    else:
        order = Order.objects.first()  # Default to the first order if no ID is given

    if not order:
        return JsonResponse({
            'status': False,
            'message': 'Order not found',
            'data': None
        }, status=404)

    # Serialize order data manually
    order_data = {
        "order_id": order.order_id,
         'total_paid': order.total_paid,
            'pages_selected': order.pages_selected,
            'is_singleside': order.is_singleside,
            'is_color': order.is_color,
            'no_copy': order.no_copy,
            'page_type': order.page_type,
            'recipt_file': order.recipt_file if order.recipt_file else "N/A",
            'date_paid': order.date_paid.strftime('%b. %d, %Y, %I:%M %p') if order.date_paid else "N/A",
            'date_printed': order.date_printed.strftime('%b. %d, %Y, %I:%M %p') if order.date_printed else "N/A",
            'is_paid': order.is_paid,
            'trx_id': order.trx_id if order.trx_id else "N/A",
            'kiosk_location_name': order.kiosk_location_name,
            'printer_name': order.printer_name,
            'printer_id': order.printer_id,
            'kiosk_id': order.kiosk_id if order.kiosk_id else "N/A",
            'mobile_device_id': order.mobile_device_id if order.mobile_device_id else "N/A",
            'file_name': order.file_name,
            'order_status': order.order_status,
            'created_at': order.created_at.strftime('%b. %d, %Y, %I:%M %p') if order.created_at else "N/A",
        
       
    }

    return JsonResponse({
        'status': True,
        'message': 'successful print',
        'order': order_data
    })