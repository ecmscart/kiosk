from django.urls import path
from django.contrib.auth import views as auth_views
from app1.views import *

urlpatterns = [
  
    path('location/', locationList, name='location'),
    path('printer/', printerList, name='printer'),
    path('cost/', costList, name='cost'),
    path('createorder/', create_order, name='create_order'),
    path('create-payment-intent/', create_payment_intent, name='create_payment_intent'),
    path('upload-image/', upload_image, name='upload_image'),
    path('set-cors/', set_bucket_cors, name='set_cors'),
    path('verifypayment/',verify_payment,name='verify_payment'),
    path('orderlist/',orderlist,name='orderlist'),
    path('orderbyid/',orderbyid,name='orderbyid'),
    
    
]