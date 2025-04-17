from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


def account_form(request, form_class, template_name, success_url, title, button_text):
    form = form_class(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save() if isinstance(form, UserCreationForm) else form.get_user()
        login(request, user)
        return redirect(success_url)
    return render(request, template_name, {'form': form, 'title': title, 'button_text': button_text})


def register_user(request):
    return account_form(
        request,
        form_class=UserCreationForm,
        template_name='accounts/account_form.html',
        success_url='home',
        title='Регистрация',
        button_text='Зарегистрироваться'
    )


def login_user(request):
    return account_form(
        request,
        form_class=AuthenticationForm,
        template_name='accounts/account_form.html',
        success_url='home',
        title='Вход',
        button_text='Войти'
    )


def logout_user(request):
    logout(request)
    return redirect('login')
