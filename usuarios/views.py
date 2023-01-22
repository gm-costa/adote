from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse


def cadastro(request):
    # template_name = 'cadastro.html'
    template_name = 'novo_usuario.html'
    if request.user.is_authenticated:
        return redirect(reverse('novo_pet'))

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
        # return redirect('/divulgar/novo_pet')
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

def recuperar_senha(request, email):
    usuario = User.objects.get(email=email)
    if not usuario:
        messages.add_message(request, messages.ERROR, f"Usuário não localizado para '{email}'.")
        return redirect(reverse('logar'))

    assunto = 'Pedido de recuperação de senha do ADOTE'
    mensagem = f"""Olá, {usuario.username}!
    
    Sua senha do ADOTE pode ser redefinida clicando no link abaixo. 
    Se você não solicitou uma nova senha, ignore este e-mail.
    
    <a href='http://127.0.0.1:8000/auth/redefinir_senha/{usuario.id}'>Redefinir senha</a>
    """

def redefinir_senha(request, id):
    pass

def sair(request):
    logout(request)
    # return redirect('/auth/login')
    return redirect(reverse('login'))
