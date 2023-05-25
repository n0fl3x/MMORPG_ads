from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import AccountCreationForm
from .models import UsersCode
from .tasks import new_user_conf_code_mail, non_activated_user_conf_code_mail


def account_register(request):
    if request.user.is_authenticated:
        return redirect('ads_list')

    if request.method == 'POST':
        form = AccountCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = user.username
            user_email = user.email

            # если не существует учётки с такой почтой
            if not User.objects.filter(email=user_email).exists():
                user.is_active = False
                user.save()
                new_user_conf_code_mail.delay(user.id)
                messages.info(
                    request,
                    'Activation code was sent to you email.')
                # создаём нового неактивного юзера и отправляем ему код
                return redirect(to='account_confirm')
            # но если учётка с такой почтой существует
            else:
                # пробуем достать её
                existing_email_user = User.objects.get(email=user_email)
                # если имена не совпали и учётка активирована
                if existing_email_user.username != username and existing_email_user.is_active:
                    form = AccountCreationForm()
                    messages.info(
                        request,
                        "Account with this email already exists.")
                    context = {
                        'reg_form': form,
                    }
                    return render(
                        request,
                        'accounts/register.html',
                        context=context,
                    )
                # если имена не совпали, но учётка не активирована
                elif existing_email_user.username != username and not existing_email_user.is_active:
                    existing_email_user.username = username
                    existing_email_user.save()
                    non_activated_user_conf_code_mail.delay(existing_email_user.id)
                    messages.info(
                        request,
                        "Looks like you've already tried to register here."
                        "New activation code was sent to you email.")
                    return redirect(to='account_confirm')
    else:
        form = AccountCreationForm()

    context = {
        'reg_form': form,
    }
    return render(
        request,
        'accounts/register.html',
        context=context,
    )


def account_confirm(request):
    if request.user.is_authenticated:
        return redirect('ads_list')

    if request.method == 'POST':
        code = request.POST.get('conf_code')

        if UsersCode.objects.filter(code=code):
            user = UsersCode.objects.get(code=code).user
            user.is_active = True
            user.save()
            UsersCode.objects.get(code=code).delete()
            return redirect(to='account_login')
        else:
            messages.info(request, 'Confirmation code is invalid.')

    context = {}
    return render(
        request,
        'accounts/activation.html',
        context=context,
    )


def account_login(request):
    if request.user.is_authenticated:
        return redirect('ads_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect(to='ads_list')
        else:
            messages.info(request, 'Username or password is incorrect. Or your account is not activated.')

    context = {}
    return render(
        request,
        'accounts/login.html',
        context=context,
    )


def account_logout(request):
    logout(request)
    return redirect(to='account_login')
