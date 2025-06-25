from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from user.forms import RegisterForm
class UserLoginView(LoginView):
    template_name = 'login.html'

class RegisterView(CreateView):
    model = User
    success_url = reverse_lazy('login')
    form_class = RegisterForm
    template_name = 'register.html'

class AccountView(TemplateView):
    template_name = 'account.html'
    
class UserLogoutView(LogoutView):
    pass