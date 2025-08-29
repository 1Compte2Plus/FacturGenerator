from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory, formset_factory
from .models import Product, Invoice, InvoiceItem
from .forms import ProductForm, InvoiceItemFormSet  # Assurez-vous d'importer le formulaire

InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    fields=('product', 'quantity'),
    extra=1,
    can_delete=True
)

ProductFormSet = formset_factory(ProductForm, extra=1)  # Affiche 3 formulaires vides

def home(request):
    context = {
        'title': 'Hello World',
        'message': 'Welcome to Django!'
    }
    return render(request, 'main/home.django-html.html', context)

class ProductListView(ListView):
    model = Product
    template_name = 'main/product_list.django-html.html'
    context_object_name = 'products'
    paginate_by = 10

class ProductCreateView(CreateView):
    model = Product
    template_name = 'main/product_form.django-html.html'
    fields = ['name', 'price', 'expiration_date']
    success_url = reverse_lazy('main:product-list')  # Ajoutez le namespace 'main:'

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'main/product_form.django-html.html'
    fields = ['name', 'price', 'expiration_date']
    success_url = reverse_lazy('main:product-list')  # Ajoutez le namespace 'main:'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'main/product_confirm_delete.django-html.html'
    success_url = reverse_lazy('main:product-list')  # Ajoutez le namespace 'main:'

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'main/invoice_list.django-html.html'
    context_object_name = 'invoices'
    paginate_by = 10    

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'main/invoice_detail.django-html.html'
    context_object_name = 'invoice'

class InvoiceCreateView(CreateView):
    model = Invoice
    template_name = 'main/invoice_form.django-html.html'
    fields = []
    success_url = reverse_lazy('main:invoice-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InvoiceItemFormSet(self.request.POST)
        else:
            context['formset'] = InvoiceItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        self.object = form.save()
        formset.instance = self.object
        if formset.is_valid():
            formset.save()
            self.object.update_total()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class InvoiceUpdateView(UpdateView):
    model = Invoice
    template_name = 'main/invoice_form.django-html.html'
    fields = []
    success_url = reverse_lazy('main:invoice-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InvoiceItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = InvoiceItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        self.object = form.save()
        formset.instance = self.object
        if formset.is_valid():
            formset.save()
            self.object.update_total()  # <-- Appelé après la sauvegarde des items
        return redirect(self.success_url)

class InvoiceDeleteView(DeleteView):
    
    model = Invoice
    template_name = 'main/invoice_confirm_delete.django-html.html'
    success_url = reverse_lazy('main:invoice-list')
