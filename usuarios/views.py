import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from .models import ResetPassword
from django.shortcuts import HttpResponse


def cadastro(request):
    # template_name = 'cadastro.html'
    template_name = 'novo_usuario.html'
    if request.user.is_authenticated:
        return redirect(reverse('seus_pets'))

    if request.method == "GET":
        return render(request, template_name)
    elif request.method == "POST":
        nome = request.POST.get('nome').strip().lower()
        email = request.POST.get('email').strip().lower()
        senha = request.POST.get('senha').strip()
        confirmar_senha = request.POST.get('confirmar_senha').strip()

        if len(nome) == 0 or len(email) == 0 or len(senha) == 0 or len(confirmar_senha) == 0:
            messages.add_message(request, messages.WARNING, 'Preencha todos os campos!')
            return render(request, template_name)
        
        if senha != confirmar_senha:
            messages.add_message(request, messages.ERROR, 'As senhas não são iguais.')
            return render(request, template_name)

        try:
            User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso.')
        except:
            messages.add_message(request, messages.ERROR, 'Ocorreu um erro ao tentar salvar, tente novamente!')
            
        return render(request, template_name)

def logar(request):
    template_name = 'logar.html'
    if request.user.is_authenticated:
        return redirect(reverse('seus_pets'))
        
    if request.method == "GET":
        return render(request, template_name)
    elif request.method == "POST":
        nome = request.POST.get('nome').strip()
        senha = request.POST.get('senha').strip()

        if len(nome) == 0 or len(senha) == 0:
            messages.add_message(request, messages.WARNING, 'Preencha todos os campos!')
            return render(request, template_name)

        user = authenticate(username=nome.lower(), password=senha)

        if user is not None:
            login(request, user)
            return redirect(reverse('seus_pets'))
        else:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha inválidos!')
            return render(request, template_name, {'nome': nome, 'senha': senha})

def recuperar_senha(request):
    if request.method == "GET":
        return render(request, 'recupera_senha.html')

    elif request.method == "POST":
        email = request.POST.get('email').strip()

        usuario = User.objects.filter(email=email)

        if not usuario:
            messages.add_message(request, messages.ERROR, f"Usuário não localizado para '{email}'.")
            return redirect(reverse('recuperar_senha'))
        
        usuario = usuario.first()

        token = secrets.token_hex(32)

        query_reset = ResetPassword.objects.filter(user=usuario.id).filter(valid=True)

        if query_reset:
            for reset in query_reset:
                reset.valid = False
                reset.save()

        reset_senha = ResetPassword(user=usuario, token=token)
        reset_senha.save()

        assunto = 'Pedido de recuperação de senha do ADOTE'
        mensagem = f"""Olá, {usuario.username}!
        
        Sua senha do ADOTE pode ser redefinida clicando no link abaixo. 
        Se você não solicitou uma nova senha, ignore este e-mail.
        
        <a href='http://127.0.0.1:8000/auth/redefinir_senha/{token}'>Redefinir senha</a>
        """

        email_enviado = send_mail(
            assunto,
            mensagem,
            'suporte@teste.com',
            [email,]
        )

        if email_enviado:
            messages.add_message(request, messages.SUCCESS, f"Instruções enviada para '{email}', verifique sua caixa postal.")
        else:
            messages.add_message(request, messages.ERROR, 'Não foi possível enviar o e-mail!')

        return redirect(reverse('recuperar_senha'))

def redefinir_senha(request, token):
    if request.method == 'GET':
        return render(request, 'reset_senha.html', {'token': token})
    elif request.method == 'POST':
        senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_nova_senha')

        if len(senha) == 0 or len(confirmar_senha) == 0:
            messages.add_message(request, messages.WARNING, 'Preencha todos os campos!')
            return render(request, 'reset_senha.html')
        
        if senha != confirmar_senha:
            messages.add_message(request, messages.ERROR, 'As senhas não são iguais.')
            return render(request, 'reset_senha.html')

        obj_token = get_object_or_404(ResetPassword, token=token)

        if not obj_token.valid:
            messages.add_message(request, messages.WARNING, 'Esse token já foi utilizado!')
            return redirect(reverse('logar'))
        
        obj_token.valid = False
        obj_token.save()

        user = User.objects.get(id=obj_token.user.id)
        user.set_password(senha)
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Cadastrado nova senha efetuado com sucesso, você já pode acessar o sistema.')
        return redirect(reverse('logar'))

def sair(request):
    logout(request)
    return redirect(reverse('logar'))
