from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .forms import AccountCreationForm


def account_register(request):
    form = AccountCreationForm()
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(
                request,
                'Account was successfully created for ' + user + '.',
            )
            return redirect('account_login')

    context = {
        'reg_form': form,
    }

    return render(
        request,
        'accounts/register.html',
        context=context,
    )


def account_login(request):
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
            messages.info(request, 'Username or password is incorrect.')

    context = {}

    return render(
        request,
        'accounts/login.html',
        context=context,
    )


def account_logout(request):
    logout(request)
    return redirect(to='account_login')
