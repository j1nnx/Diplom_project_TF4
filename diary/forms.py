from django import forms

from diary.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'content')

    def __init__(self, *args, **kwargs):
        # Вызов конструктора родительского класса
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['content'].required = True
        self.fields['image'].required = True

        # Установка виджетов к полям
        self.fields['title'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'})
        self.fields['content'].widget = forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Введите содержание'})
        self.fields['image'].widget = forms.ClearableFileInput(attrs={'class': 'form-control-file'})

        self.fields['title'].label = ''  # Убираем метку
        self.fields['content'].label = ''  # Убираем метку
        self.fields['image'].label = ''  # Убираем метку
