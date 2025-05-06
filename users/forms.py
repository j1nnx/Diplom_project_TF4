from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """ Форма для регистрации нового пользователя """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        # Установка виджетов
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите e-mail'}
        )
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите пароль повторно'}
        )


class UserProfileForm(UserChangeForm):
    """ Профиль пользователя """

    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'avatar', 'fullname', 'username')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class ResetPasswordForm(forms.ModelForm):
    """ Форма для сброса пароля """

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите e-mail'
    }))

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        print(self.fields)

        # Установка виджетов
        self.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите e-mail'}
        )


class UserAuthForm(AuthenticationForm):
    """ Форма авторизации пользователя """

    class Meta:
        model = User
        fields = ('email', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserAuthForm, self).__init__(*args, **kwargs)

        # Установка виджета
        self.fields['username'].widget = forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите e-mail'}
        )
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}
        )
