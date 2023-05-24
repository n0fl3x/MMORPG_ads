from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import AccountCreationForm
from .passwords import one_time_password
from .models import UsersCode


def account_register(request):
    if request.user.is_authenticated:
        return redirect('ads_list')

    if request.method == 'POST':
        form = AccountCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = user.username
            user_email = user.email

            if not User.objects.filter(email=user_email).exists():
                user.is_active = False
                user.save()
                conf_code = one_time_password()
                UsersCode.objects.create(user=user, code=conf_code)
                mail_subj = 'Acccount confirmation'
                to_email = form.cleaned_data.get('email')
                message = render_to_string(
                    template_name='accounts/account_activate_email.html',
                    context={
                        'username': user.username,
                        'conf_code': conf_code,
                    },
                )
                email = EmailMessage(
                    subject=mail_subj,
                    body=message,
                    to=[to_email],
                )
                email.send()
                messages.info(request, 'Activation code sent to you email.')
                return redirect(to='account_confirm')
            else:
                non_activated_user = User.objects.get(email=user_email)
                non_activated_user.username = username
                non_activated_user.save()
                new_conf_code = one_time_password()
                old_conf_code = UsersCode.objects.get(user=non_activated_user)
                old_conf_code.code = new_conf_code
                old_conf_code.save()
                mail_subj = 'New confirmation code'
                to_email = form.cleaned_data.get('email')
                message = render_to_string(
                    template_name='accounts/account_activate_email.html',
                    context={
                        'username': user.username,
                        'conf_code': new_conf_code,
                    },
                )
                email = EmailMessage(
                    subject=mail_subj,
                    body=message,
                    to=[to_email],
                )
                email.send()
                messages.info(request, 'New activation code sent to you email.')
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
