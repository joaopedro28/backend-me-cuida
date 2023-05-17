from django.views.generic import DeleteView
from django.http import HttpResponseRedirect

class SoftDeleteView(DeleteView):
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.status = False
        self.object.save()
        return HttpResponseRedirect(success_url)
