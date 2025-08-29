from django import forms
from django.forms import inlineformset_factory
from .models import Product, Invoice, InvoiceItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'expiration_date']

InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    fields=('product', 'quantity'),
    extra=1,
    can_delete=True
)