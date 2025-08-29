from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total(self):
        total = sum(item.product.price * item.quantity for item in self.items.all())
        self.total = total
        self.save(update_fields=['total'])

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def price(self):
        return self.product.price

    @property
    def subtotal(self):
        return self.product.price * self.quantity
