from django.views import generic
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy

from products.models import Product
from checkout.forms import CheckoutOrderCreateForm


class CheckoutCartView(generic.TemplateView):
    template_name = 'checkout/cart.html'
    http_method_names = ['get', 'post', 'delete', 'head'] 
    
    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()

        if method == 'delete':
            return self.delete(*args, **kwargs)
        
        return super(CheckoutCartView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart'] = self.request.cart

        return context
    
    def delete(self, *args, **kwargs):  
        product_id = self.request.POST.get('delete_product')
        product = get_object_or_404(Product, id=product_id)
        self.request.cart.remove(product)
        
        return redirect('checkout:cart')


# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
from django.contrib.auth import get_user_model

from checkout.models import OrderItem

class CheckoutServices:
    def __init__(self):
        self.User = get_user_model()

    def create_order_item(self, order, product, price, size, color, quantity):
        item = OrderItem.objects.create(
            order=order,
            product=product,
            price=price,
            size=size,
            color=color,
            quantity=quantity,
        )
        return item
    
    def get_user_by_username(self, username):
        user = self.User.objects.get(username=username)
        return user
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX

class CheckoutView(generic.FormView):
    template_name = 'checkout/checkout.html'
    success_url = reverse_lazy('checkout:checkout')
    form_class = CheckoutOrderCreateForm
    
    def setup(self, request, *args, **kwargs):
        super(CheckoutView, self).setup(request, *args, **kwargs)
        self.service = CheckoutServices()

    def get_initial(self):
        initial = super(CheckoutView, self).get_initial()
        initial.update(
            {
                'first_name': getattr(self.request.user, 'first_name', ''),
                'last_name': getattr(self.request.user, 'last_name', ''),
                'email': getattr(self.request.user, 'email', ''),
                'phone_number': getattr(self.request.user, 'phone_number', ''),
                'price': getattr(self.request.user, 'price', ''),
            }
        )
        return initial
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:

            cleaned_data = form.cleaned_data
            self._save_account_data(cleaned_data, self.request.user.username)
            
            order = form.save(commit=False)
            order.user = self.request.user
            order.save()
        else:
            order = form.save()

        for item in self.request.cart:
            self.service.create_order_item(
                order=order,
                product=item['product'],
                price=item['price'],
                size=item['size'],
                color=item['color'],
                quantity=item['quantity'],
            )

        self.request.cart.clear()
        messages.success(self.request, 'Order created successfully.')
        
        return super(CheckoutView, self).form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for error in form.errors.values():
                messages.error(self.request, error)
        else:
            messages.error(self.request, 'Order creation failed.')
            
        return super(CheckoutView, self).form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        context['cart'] = self.request.cart

        return context
    
    def _save_account_data(self, form_data, username):
        user = self.service.get_user_by_username(username=username)
        user.first_name = user.first_name or form_data['first_name']
        user.last_name = user.last_name or form_data['last_name']
        user.phone_number = user.phone_number or form_data['phone_number']
        user.save()
