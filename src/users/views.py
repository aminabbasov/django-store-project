from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from checkout.models import Order
from users.forms import UsersAccountForm
from users.forms import UsersLoginForm
from users.forms import UsersPasswordChangeForm
from users.forms import UsersRegisterForm
from users.models import User
from users.services import UserUpdater


class UsersRegisterView(SuccessMessageMixin, generic.FormView):
    template_name = "users/register.html"
    form_class = UsersRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("users:account")
    success_message = "You have successfully registered!"

    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)

        return super(UsersRegisterView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:index")

        return super(UsersRegisterView, self).get(request, *args, **kwargs)


class UsersLoginView(SuccessMessageMixin, LoginView):
    template_name = "users/login.html"
    form_class = UsersLoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("users:index")
    success_url = reverse_lazy("users:account")
    success_message = "You have successfully logged in!"

    def setup(self, request, *args, **kwargs):
        super(UsersLoginView, self).setup(request, *args, **kwargs)
        self.just_logged_in = False

    def form_valid(self, form):
        if self.request.POST.get("remember_me", False):
            self.request.session.set_expiry(settings.KEEP_LOGGED_DURATION)

        self.just_logged_in = True
        return super(UsersLoginView, self).form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for error in form.errors.values():
                messages.error(self.request, error)

        return super(UsersLoginView, self).form_invalid(form)

    def get_success_url(self):
        if self.just_logged_in:
            return self.success_url
        return self.next_page


class UsersAccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = "users/account.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UsersAccountView, self).get_context_data(*args, **kwargs)
        context["password_form"] = UsersPasswordChangeForm(user=self.request)
        context["account_form"] = UsersAccountForm(self.request.user)
        context["orders"] = Order.objects.filter_by_user(user=self.request.user.pk)

        return context


class UsersPasswordChangeView(PasswordChangeView):
    template_name = "users/account.html"
    http_method_names = ["post"]
    form_class = UsersPasswordChangeForm
    success_url = reverse_lazy("users:account")

    def get_form_kwargs(self):
        kwargs = super(UsersPasswordChangeView, self).get_form_kwargs()

        if self.request.method.lower() == "post":
            kwargs["user"] = self.request.user
            kwargs["data"] = self.request.POST

        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Password successfully changed!")

        return super(UsersPasswordChangeView, self).form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for error in form.errors.values():
                messages.error(self.request, error)

        return redirect("users:account")


class UsersAccountEditView(LoginRequiredMixin, generic.FormView):
    template_name = "users/account.html"
    http_method_names = ["post"]
    form_class = UsersAccountForm
    success_url = reverse_lazy("users:account")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        user = self.request.user
        username = cleaned_data["username"]

        if User.objects.is_username_available(username=username):
            if any(cleaned_data.values()):
                UserUpdater(user=user, user_data=cleaned_data)()
                messages.success(self.request, "Your account has been successfully edited!")
            else:
                messages.info(self.request, "You have not entered any data to change.")
        else:
            if user.username == username:
                messages.error(self.request, f"You are already using {username} username.")
            else:
                messages.error(self.request, f"Username {username} is not available.")

        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for error in form.errors.values():
                messages.error(self.request, error)

        return redirect("users:account")
