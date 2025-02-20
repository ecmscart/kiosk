from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.cloud import storage
from django.conf import settings
import os
from datetime import datetime

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # Initialize Google Cloud Storage client
            client = storage.Client.from_service_account_json(settings.GS_CREDENTIALS)
            bucket = client.bucket(settings.GS_BUCKET_NAME)

            # Get the uploaded file
            uploaded_file = request.FILES['image']
            file_name = uploaded_file.name

            # Generate a unique file name to avoid conflicts
            unique_file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file_name}"

            # Upload the file to GCS
            blob = bucket.blob(unique_file_name)
            blob.upload_from_file(uploaded_file)

            # Get the public URL of the uploaded file
            public_url = blob.public_url

            return JsonResponse({
                'message': 'File uploaded successfully!',
                'public_url': public_url,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request or no file uploaded'}, status=400)

def set_bucket_cors(request,bucket_name='kiosk-bucket'):
    try:
        # Specify the path to your service account key file
        #credentials_path = settings.GS_CREDENTIALS
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        # Initialize the client using explicit credentials
        client = storage.Client.from_service_account_json(settings.GS_CREDENTIALS)
        bucket = client.bucket(bucket_name)

        # Define the CORS configuration
        cors = [
            {
                "origin": ["*"],
                "method": ["PUT"],
                "responseHeader": ["Content-Type"],
                "maxAgeSeconds": 3600
            }
        ]

        # Set the CORS configuration
        bucket.cors = cors
        bucket.patch()

        print(f"Set CORS configuration for bucket {bucket_name}.")
        return JsonResponse({'success': 'success'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)