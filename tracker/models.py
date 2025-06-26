from django.db import models

class TrackedProduct(models.Model):
    email = models.EmailField()
    product_url = models.URLField()
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} | {self.product_url} | ₹{self.target_price}"
