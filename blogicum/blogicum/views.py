from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:index')
