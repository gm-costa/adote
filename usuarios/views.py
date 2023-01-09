from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'Preencha todos os campos!')
            return render(request, 'cadastro.html')
        
        if senha != confirmar_senha:
            messages.add_message(request, messages.ERROR, 'As senhas não são iguais.')
            return render(request, 'cadastro.html')

        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso.')
            # return render(request, 'cadastro.html')
        except:
            messages.add_message(request, messages.ERROR, 'Ocorreu um erro ao tentar salvar, tente novamente!')
            
        return render(request, 'cadastro.html')
