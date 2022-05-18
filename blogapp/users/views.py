from django.contrib import messages
from django.contrib.auth.models import Permission
from django.views.generic import FormView

from users.forms import NewWriterForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = NewWriterForm
    success_url = '/'

    def form_valid(self, form):
        writer = form.save()
        # This is used just for now !!!!
        permissions = Permission.objects.all()
        writer.user_permissions.set(permissions)
        messages.success(self.request, "Account created. You can now log in.")
        return super().form_valid(form)
