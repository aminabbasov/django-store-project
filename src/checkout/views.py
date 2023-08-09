from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from checkout.forms import CheckoutOrderCreateForm
from checkout.services import OrderItemCreator
from products.models import Product
from products.models import ProductView
from users.models import User


class CheckoutBasketView(generic.TemplateView):
    template_name = "checkout/basket.html"
    http_method_names = ["get", "post", "delete", "head"]

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get("_method", "").lower()

        if method == "delete":
            return self.delete(*args, **kwargs)

        return super(CheckoutBasketView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        public_ids = list(map(int, self.request.basket.keys()))
        context["basket_and_products"] = zip(
            self.request.basket.values(), ProductView.objects.filter(variant_id__in=public_ids)
        )

        return context

    def delete(self, *args, **kwargs):
        variant_id = self.request.POST.get("delete_product")
        self.request.basket.remove(variant_id)

        return redirect("checkout:basket")


class CheckoutView(generic.FormView):
    template_name = "checkout/checkout.html"
    success_url = reverse_lazy("users:account")
    form_class = CheckoutOrderCreateForm

    def get_initial(self):
        initial = super().get_initial()
        initial.update(
            {
                "first_name": getattr(self.request.user, "first_name", ""),
                "last_name": getattr(self.request.user, "last_name", ""),
                "email": getattr(self.request.user, "email", ""),
                "phone_number": getattr(self.request.user, "phone_number", ""),
                "price": getattr(self.request.basket, "get_total_price", ""),
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

        for pk, options in self.request.basket.items():
            public_id = ProductView.objects.get(variant_id=pk).public_id
            product = Product.objects.get(public_id=public_id)
            OrderItemCreator(
                order=order,
                product=product,
                price=options["price"],
                option=options["option"],
                quantity=options["quantity"],
            )()

        self.request.basket.clear()
        messages.success(self.request, "Order created successfully.")

        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for field, error in form.errors.items():
                messages.error(self.request, f"{field} - {error}")
        else:
            messages.error(self.request, "Order creation failed.")

        return super().form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        public_ids = list(map(int, self.request.basket.keys()))
        context["basket_and_products"] = zip(
            self.request.basket.values(), ProductView.objects.filter(variant_id__in=public_ids)
        )

        return context

    def _save_account_data(self, form_data, username):
        user = User.objects.get_by_username(username)
        user.first_name = user.first_name or form_data["first_name"]
        user.last_name = user.last_name or form_data["last_name"]
        user.phone_number = user.phone_number or form_data["phone_number"]
        user.save()
