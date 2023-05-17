from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.models import HealthProfile

class NotPatientMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        temp = super().dispatch(request, *args, **kwargs)
        if not (HealthProfile.objects.filter(user=self.request.user, status=True) or self.request.user.is_superuser):
            return self.handle_no_permission()
        return temp

class SuperorAdminMixin(NotPatientMixin):
    def dispatch(self, request, *args, **kwargs):
        temp = super().dispatch(request, *args, **kwargs)
        if not (self.request.user.is_superuser or HealthProfile.objects.filter(user=self.request.user, admin=True, status=True)):
            return self.handle_no_permission()
        return temp
