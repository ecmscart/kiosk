from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app1.models import PriceMatrix
from django.utils.timezone import now


@login_required
def price_cost_list(request):
    price_cost = PriceMatrix.objects.all()
    return render(request, 'admin/print_cost/print_cost.html',{'price_cost': price_cost})

@login_required
def display_cost(request):
    draw = int(request.GET.get('draw', 1))  # Draw counter to keep track of DataTable requests
    start = int(request.GET.get('start', 0))  # The starting point of the data (pagination)
    length = int(request.GET.get('length', 10))  # The number of records per page
    search_value = request.GET.get('search[value]', '').strip()  # Search keyword

    price_cost = PriceMatrix.objects.all()
    if search_value:
        price_cost = price_cost.filter(name__icontains=search_value)

    order_column = int(request.GET.get('order[0][column]', 0))  # Column index for sorting
    order_dir = request.GET.get('order[0][dir]', 'DESC')
    if order_column == 0:
        price_cost = price_cost.order_by('-id')

    price_cost_paginated = price_cost[start:start+length]
    data = [
        {   'id': price_cost.id,
            'page_type': price_cost.page_type,
            'min_page': price_cost.min_page,
            'max_page': price_cost.max_page,
            'black_price': price_cost.black_price,
            'color_price': price_cost.color_price,
            'status': price_cost.status,
            'created_at': price_cost.created_at.strftime('%b. %d, %Y, %I:%M %p') if price_cost.created_at else "N/A",  # Handle None
        }
        for price_cost in price_cost_paginated
    ]
    records_total = PriceMatrix.objects.count()  
    records_filtered = price_cost.count()
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
def create_cost(request):
    if request.is_ajax():
        try:
            # Parse POST data
            page_type= request.POST.get('page_type')
            min_page= request.POST.get('min_page')
            max_page= request.POST.get('max_page')
            black_price= request.POST.get('black_price')
            color_price= request.POST.get('color_price')
            status = request.POST.get('status')

            # Validate inputs
            if not page_type or not min_page or not max_page or not black_price or not color_price or status not in ['0', '1']:
                return JsonResponse({'error': 'Invalid input data'}, status=400)

            # Create the location
            price_cost = PriceMatrix.objects.create(
                page_type=page_type,
                min_page=min_page,
                max_page=max_page,
                black_price=black_price,
                color_price=color_price,
                status=status,
                created_at=now()  # Set the current timestamp
            )

            # Respond with the newly created location's data
            return JsonResponse({
                'message': 'Cost created successfully',
                'price_cost': {
                    'id': price_cost.id,
                    'page_type': price_cost.page_type,
                    'min_page': price_cost.min_page,
                    'max_page': price_cost.max_page,
                    'black_price': price_cost.black_price,
                    'color_price': price_cost.color_price,
                    'status': price_cost.status,
                    'created_at': price_cost.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# API for deleting a cost (AJAX)
@login_required
def delete_cost(request, id):
    if request.is_ajax():
        price_cost = PriceMatrix.objects.get(id=id)
        price_cost.delete()
        return JsonResponse({'message': 'Cost deleted successfully'})
    
# API for editing a cost (AJAX)
@login_required
def edit_cost(request, id):
    price_cost = get_object_or_404(PriceMatrix, id=id)
    
    if request.method == 'POST' and request.is_ajax():
         page_type= request.POST.get('page_type')
         min_page= request.POST.get('min_page')
         max_page= request.POST.get('max_page')
         black_price= request.POST.get('black_price')
         color_price= request.POST.get('color_price')
         status = request.POST.get('status')

        # Update the location fields
         price_cost.page_type = page_type
         price_cost.min_page = min_page
         price_cost.max_page = max_page
         price_cost.black_price = black_price
         price_cost.color_price = color_price
         price_cost.status = status

        # Save the updated location
         price_cost.save()

        # Return the updated location details in the response
         return JsonResponse({
            'message': 'Cost updated successfully',
            'cost': {
                'id': price_cost.id,
                'page_type': price_cost.page_type,
                'min_page': price_cost.min_page,
                'max_page': price_cost.max_page,
                'black_price': price_cost.black_price,
                'color_price': price_cost.color_price,
                'status': price_cost.status,
                'created_at': price_cost.created_at.strftime('%b. %d, %Y, %I:%M %p')
                
            }
        })
    

def costList(request):
    if request.method == 'GET':
        size = request.GET.get('size')
        totalpage = request.GET.get('totalpage')
        # Validate that size is provided
        if not size:
            return JsonResponse({'status': False, 'message': 'Size parameter is required', 'data': {}})
        
        if not totalpage:
            return JsonResponse({'status': False, 'message': 'Total page parameter is required', 'data': {}})

        # Fetch the latest active price cost based on size
        price_cost = PriceMatrix.objects.filter(status=1, page_type=size,min_page__lte=totalpage,max_page__gte=totalpage).order_by('-id').values().first()

        if price_cost:
            # Set price based on color flag
           price_cost['price'] = price_cost['black_price'] if request.GET.get('color') == '1' else price_cost['color_price']

           price_cost_data = {
                'status': True,
                'message': 'success',
                'data': price_cost
            }
        else:
            price_cost_data = {
                'status': False,
                'message': 'No cost found',
                'data': {}
            }

        return JsonResponse(price_cost_data)


