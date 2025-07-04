from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from .forms import RegistroUsuarioForm
from django.urls import reverse

class CustomLoginView(LoginView):
    template_name = "auth/login.html"

class CustomPasswordResetView(PasswordResetView):
    template_name = "auth/password_reset_form.html"

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "auth/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def registro_usuario(request):
    form = RegistroUsuarioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        grupo = Group.objects.get(name='Encargado')
        user.groups.add(grupo)
        return redirect('login')
    return render(request, 'auth/registro.html', {'form': form})

def valida_user(request):
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
        else:
            messages.info(request, 'Credenciales incorrectas')
    return redirect('/app_biblioteca/')

def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = get_random_string(32)
            request.session['password_reset_token'] = token
            request.session['password_reset_user'] = user.pk
            link = request.build_absolute_uri(f'/app_biblioteca/reset_password/{token}/')
            send_mail(
                'Recupera tu contraseña',
                f'Hola {user.username}, haz clic en el siguiente enlace para restablecer tu contraseña: {link}',
                None,
                [email]
            )
            messages.success(request, 'Enlace enviado a tu correo.')
            return redirect('custom_password_reset')
        except User.DoesNotExist:
            messages.error(request, 'Correo no registrado.')
    return render(request, 'auth/custom_password_reset.html')

def custom_password_reset_confirm(request, token):
    session_token = request.session.get('password_reset_token')
    user_id = request.session.get('password_reset_user')
    if not session_token or session_token != token or not user_id:
        return render(request, 'auth/custom_password_reset_invalid.html')

    if request.method == 'POST':
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        if p1 != p2:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif len(p1) < 8 or p1.isdigit():
            messages.error(request, 'Contraseña inválida.')
        else:
            user = User.objects.get(pk=user_id)
            user.password = make_password(p1)
            user.save()
            del request.session['password_reset_token']
            del request.session['password_reset_user']
            messages.success(request, 'Contraseña cambiada. Inicia sesión.')
            return redirect('login')
    return render(request, 'auth/custom_password_reset_confirm.html')