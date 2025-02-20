from django.db import models

class PriceMatrix(models.Model):
    id = models.AutoField(primary_key=True)
    PAGE_TYPE_CHOICES = [
        ('A3', 'A3'),
        ('A4', 'A4'),
    ]

    page_type = models.CharField(max_length=2, choices=PAGE_TYPE_CHOICES)
    min_page = models.IntegerField(default=0)
    max_page = models.IntegerField(default=0)
    black_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    color_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=1, default='1')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "price_matrix"
