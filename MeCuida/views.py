from django.http.response import HttpResponseRedirect
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import TemplateView, UpdateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from profiles.models import HealthProfile, PatientProfile

UserModel = get_user_model()

def user_context(request):
    usertype = 'Anônimo'
    priority = 0
    profile = None
    try:
        profile = HealthProfile.objects.get(status=True, user=request.user)
        if profile.admin:
            usertype = 'Administrador'
            priority = 3
        else:
            usertype = 'Profissional de Saúde'
            priority = 2
    except:
        try:
            profile = PatientProfile.objects.get(status=True, user=request.user)
            usertype = 'Paciente'
            priority = 1
        except:
            if not request.user.is_anonymous and request.user.is_superuser:
                usertype = 'Super-Usuário'
                priority = 4
    return {
        'usertype': usertype,
        'priority': priority,
        'profile': profile
    }

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "layout.html"

# Views autenticação
class LoginView(LoginView):
    template_name = "login.html"

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))

class SelfDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'self_detail.html'

class SelfUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'self_update.html'
    fields = ['username', 'email']
    success_url = '/detail/'

    def get_object(self):
        return self.request.user

class PasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = '/detail/'
