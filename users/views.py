import random
import secrets
import string

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, FormView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, ResetPasswordForm
from users.models import User


def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')


class RegisterView(CreateView):
    """ Регистрация нового пользователя с подтверждением через email """

    model = User
    form_class = UserRegisterForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email, ]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        # Возвращаем текущего пользователя, чтобы обновить его профиль
        return self.request.user

    def form_valid(self, form):
        # Здесь можно добавить логику, которая срабатывает при успешной валидации формы
        return super().form_valid(form)


class UserPasswordResetView(FormView):
    """ Контроллер для восстановления пароля """

    template_name = 'users/reset_password_form.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user:
                password = ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])
                user.set_password(password)
                user.is_active = True
                user.save()
                send_mail(
                    subject='Сброс пароля',
                    message=f" Ваш новый пароль {password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            return super().form_valid(form)
        except:
            return redirect(reverse('users:registration'))


class UserInValidEmail(TemplateView):
    """ Контроллер отработки исключения, когда нет пользователя с таким email """

    template_name = 'users:invalid_email'
