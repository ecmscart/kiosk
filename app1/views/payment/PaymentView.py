import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

# Set your Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY
print(settings.STRIPE_SECRET_KEY)
@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
                if request.content_type == 'application/json':
                        data = json.loads(request.body)  # Parse JSON request
                else:
                        data = request.POST  # Parse form data
                    
                        print("Received Data:", data)  # Debugging

                # Validate the 'amount' field
                amount_str = data.get('amount')
                if not amount_str:
                        return JsonResponse({'error': 'Amount is required'}, status=400)
                try:
                    # Parse the request body
                    # data = request.POST
                    amount = int(float(amount_str) * 100)  # Convert to cents
                except ValueError:
                        return JsonResponse({'error': 'Invalid amount value'}, status=400)
                currency = 'USD'

                # Create a PaymentIntent
                payment_intent = stripe.PaymentIntent.create(
                        amount=amount,
                        currency=currency,
                        automatic_payment_methods={'enabled': True},
                    )

                # Return the PaymentIntent client secret
                return JsonResponse({
                        'client_secret': payment_intent.client_secret,
                        'id': payment_intent.id,
                    })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def verify_payment(request):
    data = request.GET
    print(data)
    try:
        payment_intent_id = data.get("payment_intent_id")
        # Retrieve the payment intent from Stripe
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        print(payment_intent)
        # Get the status of the payment
        payment_status = payment_intent.status

        if payment_status == "succeeded":
                    message = "Payment Successful!"
        elif payment_status == "requires_payment_method":
                    message = "Payment requires a valid payment method. Please retry with a different card."
        elif payment_status == "requires_action":
            message = "Additional authentication required. Please complete the payment process."
        elif payment_status == "processing":
            message = "Payment is still processing. Please check again later."
        else:
            message = f"Payment Status: {payment_status}"
        # Response data
        response_data = {
            "payment_status": payment_status,
            "message": message
        }

        return JsonResponse(response_data)

    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
