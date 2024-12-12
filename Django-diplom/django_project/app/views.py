from django.shortcuts import render, redirect
from .models import User  # Импортируем модель пользователя
from .forms import UserRegister  # Импортируем форму регистрации
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password  # Импортируем функции для хеширования паролей

def sign_up_by_django(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']

            if not User.objects.filter(username=username).exists():  # Проверяем, существует ли пользователь
                if password == repeat_password:
                    hashed_password = make_password(password)  # Хешируем пароль
                    User.objects.create(username=username, email=email, password=hashed_password)  # Сохраняем пользователя
                    messages.success(request, f'Приветствуем, {username}!')
                    return redirect('login')  # Перенаправляем на страницу входа
                else:
                    messages.error(request, 'Пароли не совпадают')
            else:
                messages.error(request, 'Пользователь уже существует')
    else:
        form = UserRegister()

    context = {'form': form}
    return render(request, 'registration_page.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)  # Получаем пользователя из базы данных
            if check_password(password, user.password):  # Проверяем пароль
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')  # Перенаправляем на главную страницу
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')  # Сообщение об ошибке
        except User.DoesNotExist:
            messages.error(request, 'Неверное имя пользователя или пароль.')  # Сообщение об ошибке

    return render(request, 'login.html')  # Отображаем страницу входа
