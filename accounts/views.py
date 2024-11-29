from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
# Aquí comienza
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
User = get_user_model()


# Aquí termina

from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView)  # Añadido



from .forms import (
    CustomUserCreationForm,
    UserUpdateForm,
)  # Modificado
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)  # Modificado
from django.urls import reverse  # Añadido

from django.contrib.auth import logout

class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser
    


def exit_sesion(request):
    logout(request)
    return redirect('/accounts/login')

class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tasks:index")


    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=raw_pw)
        login(self.request, user)
        return response
 


# Aquí comienza
class UserDetail(OnlyYouMixin , DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
# Aquí termina


# Omitido
class UserUpdate(OnlyYouMixin , UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_edit.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.kwargs['pk']})


#password
class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/user_detail.html'
 
class UserDelete(OnlyYouMixin , DeleteView):
    model = User
    template_name = 'accounts/user_delete.html'
    success_url = reverse_lazy('login')

