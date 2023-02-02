from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from divulgar.models import Pet, Raca
from .models import PedidoAdocao
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail


@login_required
def listar_pets(request):
    if request.method == "GET":
        # Obtém as solicitações do usuário logado
        pedidos = PedidoAdocao.objects.filter(status='AG').filter(usuario_id=request.user.id)
        pedidos = [p.pet_id for p in pedidos]

        pets = Pet.objects.filter(status="P").exclude(usuario=request.user)

        # Excluir pets solicitados pelo mesmo usuário
        pets = pets.exclude(id__in=pedidos)

        racas = Raca.objects.all()

        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        if cidade:
            pets = pets.filter(cidade__icontains=cidade)

        if raca_filter:
            pets = pets.filter(raca__id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)

        context = {
            'usuario': request.user.username,
            'pets': pets, 
            'racas': racas, 
            'cidade': cidade, 
            'raca_filter': raca_filter}

        return render(request, 'listar_pets.html', context)

@login_required
def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status="P")

    if not pet.exists():
        messages.add_message(request, messages.WARNING, 'Esse pet já foi adotado :)')
        return redirect(reverse('listar_pets'))

    pedido = PedidoAdocao(
        pet=pet.first(),
        usuario=request.user,
        data=datetime.now())

    pedido.save()

    messages.add_message(request, messages.SUCCESS, 'Pedido de adoção realizado, você receberá um e-mail caso ele seja aprovado.')
    return redirect(reverse('listar_pets'))

@login_required
def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    pet = Pet.objects.get(id=pedido.pet.id)

    if status == "A":
        pedido.status = 'AP'
        pet.status = 'A'
        string = '''Olá, sua adoção foi aprovada. ...'''
    elif status == "R":
        string = '''Olá, sua adoção foi recusada. ...'''
        pedido.status = 'R'

    #TODO: implantar transaction atomic, e automaticamente recusar as outras solicitações para este pet

    pedido.save()
    if status == "A":
        pet.status = 'A'
        pet.save()

        solicitacoes = PedidoAdocao.objects.filter(pet_id=pet.id).exclude(usuario_id=pedido.usuario.id)
        if solicitacoes:
            for solicitacao in solicitacoes:
                solicitacao.status='R'
                solicitacao.save()
                send_mail(
                    'Sua adoção foi processada',
                    '''Adoção do pet concedida a outro, levando em considereção diversos motivos, 
                    entre eles a data/hora da solicitação.''',
                    request.user.email,
                    [solicitacao.usuario.email,]
                )
        
    email = send_mail(
        'Sua adoção foi processada',
        string,
        request.user.email,
        [pedido.usuario.email,]
    )
    
    messages.add_message(request, messages.SUCCESS, 'Pedido de adoção processado com sucesso.')
    return redirect(reverse('ver_pedido_adocao'))
