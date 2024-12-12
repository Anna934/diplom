from django import forms

class UserRegister(forms.Form):
    username = forms.CharField(max_length=30, label='Введите логин: ')  # Поле для ввода имени пользователя
    email = forms.EmailField(label='Введите электронную почту: ')  # Поле для ввода электронной почты
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Введите пароль: ')  # Поле для ввода пароля
    repeat_password = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Повторите пароль: ')  # Поле для повторного ввода пароля

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data

class UserLogin(forms.Form):
    username = forms.CharField(max_length=30, label='Введите логин: ')  # Поле для ввода имени пользователя
    password = forms.CharField(widget=forms.PasswordInput, label='Введите пароль: ')  # Поле для ввода пароля
