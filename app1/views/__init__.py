from .admin_dashboard_view import is_admin,admin_dashboard
from .kiosk_location.KioskLocationView import kiosk_location_list,location_ajax_list,edit_location,delete_location,create_location,locationList
from .kiosk_printer.KioskPrinterView import kiosk_printer_list,display_printer,delete_printer,printerList,edit_printer,create_printer
from .print_cost.PrintCostView import price_cost_list,display_cost,create_cost,delete_cost,edit_cost,costList
from .orders.OrderViews import *
from .payment.PaymentView import *
from .upload_image.UploadImageView import upload_image,set_bucket_cors
