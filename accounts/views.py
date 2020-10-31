from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if user:
        auth.login(request, user)
        messages.success(request, 'Bem vindo!!!')
        return redirect('dashboard')
    else:
        messages.error(request, 'Usuario ou senha invalidos')
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'Logout realizado com sucesso')
    return redirect('login')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not usuario or not email or not senha or not senha2:
        messages.error(request, 'Preencha todos os campos')
        return render(request, 'accounts/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email invalido')
        return render(request, 'accounts/cadastro.html')

    if len(senha) < 6:
        messages.error(request, 'Senha deve ter 6 ou mais caracteres')
        return render(request, 'accounts/cadastro.html')

    if len(usuario) < 6:
        messages.error(request, 'Usuario deve ter 6 ou mais caracteres')
        return render(request, 'accounts/cadastro.html')

    if senha != senha2:
        messages.error(request, 'A senhas nao conferem')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuario já existe')
        return render(request, 'accounts/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já cadastrado')
        return render(request, 'accounts/cadastro.html')

    messages.success(request, 'Usuario cadastrado com sucesso')
    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
