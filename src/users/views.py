from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from users.forms import (
    WebsiteRegisterForm, WebsiteLoginForm, WebsitePasswordChangeForm, WebsiteAccountForm
)


class WebsiteRegisterView(SuccessMessageMixin, FormView):
    template_name = 'users/register.html'
    form_class = WebsiteRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('users:account')
    success_message = 'You have successfully registered!'
    
    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)

        return super(WebsiteRegisterView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:index')

        return super(WebsiteRegisterView, self).get(request, *args, **kwargs)


class WebsiteLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = WebsiteLoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy('users:index')
    success_url = reverse_lazy('users:account')
    success_message = 'You have successfully logged in!'
    
    def setup(self, request, *args, **kwargs):
        super(WebsiteLoginView, self).setup(request, *args, **kwargs)
        self.just_logged_in = False
    
    def form_valid(self, form):
        if self.request.POST.get('remember_me', False):
            self.request.session.set_expiry(settings.KEEP_LOGGED_DURATION)

        self.just_logged_in = True
        return super(WebsiteLoginView, self).form_valid(form)
    
    def form_invalid(self, form):
        if form.errors:
            for error in form.errors.values():
                messages.error(self.request, error)
        
        return super(WebsiteLoginView, self).form_invalid(form)
    
    def get_success_url(self):
        if self.just_logged_in:
            return self.success_url
        return self.next_page


# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# class AccountServices:
#     def get_orders_by_user(self, user):
#         filtered_orders = Order.objects.annotate().filter(user=user)
#         return filtered_orders
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX

class WebsiteAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'
    
    def setup(self, request, *args, **kwargs):
        super(WebsiteAccountView, self).setup(request, *args, **kwargs)
        #! self.service = AccountServices()                                                 # XXX XXX XXX XXX XXX XXX
    
    def get_context_data(self, *args, **kwargs):
        context = super(WebsiteAccountView, self).get_context_data(*args, **kwargs)
        context['password_form'] = WebsitePasswordChangeForm(user=self.request)
        context['account_form'] = WebsiteAccountForm(self.request.user)
        context['orders'] = self.service.get_orders_by_user(user=self.request.user.pk)

        return context


class WebsitePasswordChangeView(PasswordChangeView):
    template_name = 'users/account.html'
    http_method_names = ['post']
    form_class = WebsitePasswordChangeForm
    success_url = reverse_lazy('users:account')
    
    def get_form_kwargs(self):
        kwargs = super(WebsitePasswordChangeView, self).get_form_kwargs()

        if self.request.method.lower() == 'post':
            kwargs['user'] = self.request.user
            kwargs['data'] = self.request.POST

        return kwargs
    
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Password successfully changed!')

        return super(WebsitePasswordChangeView, self).form_valid(form)
    
    def form_invalid(self, form):
        if form.errors:
            for error in form.errors.values():
                messages.error(self.request, error)
                
        return redirect('users:account')


# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# class WebsiteAccountServices:
#     def __init__(self):
#         self.User = get_user_model()
    
#     def is_username_available(self, username):
#         is_available = self.User.objects.filter(username=username).exists()
#         return not is_available

#     def get_user_by_username(self, username):
#         user = self.User.objects.get(username=username)
#         return user
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX
# XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX --- XXX

class WebsiteAccountEditView(LoginRequiredMixin, FormView):
    template_name = 'users/account.html'
    http_method_names = ['post']
    form_class = WebsiteAccountForm
    success_url = reverse_lazy('users:account')
    
    def setup(self, request, *args, **kwargs):
        super(WebsiteAccountEditView, self).setup(request, *args, **kwargs)
        #! self.service = WebsiteAccountServices()                                          # XXX XXX XXX XXX XXX XXX

    def get_form_kwargs(self):
        kwargs = super(WebsiteAccountEditView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        if self.service.is_username_available(username=cleaned_data['username']):
        
            if any(cleaned_data.values()):
                user = self.service.get_user_by_username(username=self.request.user.username)

                user.first_name = cleaned_data['first_name'] or user.first_name
                user.last_name = cleaned_data['last_name'] or user.last_name
                user.username = cleaned_data['username'] or user.username
                user.email = cleaned_data['email'] or user.email
                user.phone_number = cleaned_data['phone_number'] or user.phone_number

                user.save()
                messages.success(self.request, 'Your account has been successfully edited!')
            else:
                messages.info(self.request, 'You have not entered any data to change.')

        elif self.request.user.username == cleaned_data['username']:
            messages.error(self.request, f"You are already using {cleaned_data['username']} username.")
        else:
            messages.error(self.request, f"Username {cleaned_data['username']} is not available.")

        return super(WebsiteAccountEditView, self).form_valid(form)
    
    def form_invalid(self, form):
        if form.errors:
            for error in form.errors.values():
                messages.error(self.request, error)
        
        return redirect('users:account')
