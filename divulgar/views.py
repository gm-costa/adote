from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from adotar.models import PedidoAdocao
from .models import Pet, Tag, Raca
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction


@login_required
def novo_pet(request):
    usuario = request.user.username
    racas = Raca.objects.all()
    if request.method == "GET":
        tags = Tag.objects.all()
        return render(request, 'novo_pet.html', {'tags': tags, 'racas': racas, 'usuario': usuario})
    elif request.method == "POST":
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome').strip()
        descricao = request.POST.get('descricao').strip()
        estado = request.POST.get('estado').strip()
        cidade = request.POST.get('cidade').strip()
        telefone = request.POST.get('telefone').strip()
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        if not foto:
            messages.add_message(request, messages.WARNING, 'Foto não selecionada !')
            return redirect(reverse('novo_pet'))

        if (len(nome) == 0) or (len(nome) == 0) or (len(nome) == 0) or (len(nome) == 0) or (len(nome) == 0):
            messages.add_message(request, messages.WARNING, 'Informe todos os campos !')
            return redirect(reverse('novo_pet'))

        if not tags:
            messages.add_message(request, messages.WARNING, 'Nenhuma tag selecionada !')
            return redirect(reverse('novo_pet'))

        if not raca:
            messages.add_message(request, messages.WARNING, 'Raça não selecionada !')
            return redirect(reverse('novo_pet'))

        pet = Pet(
            usuario=request.user,
            foto=foto,
            nome=nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca,
        )

        try:
            with transaction.atomic():
                pet.save()
                for tag_id in tags:
                    tag = Tag.objects.get(id=tag_id)
                    pet.tags.add(tag)

                tags = Tag.objects.all()
                pet.save()
                messages.add_message(request, messages.SUCCESS, 'Novo pet cadastrado com sucesso.')
        
        except Exception as e:
            messages.add_message(request, messages.ERROR, 'Não foi possível cadastrar o pet, tente novamente !')

        return render(request, 'novo_pet.html', {'tags': tags, 'racas': racas, 'usuario': usuario})

@login_required
def seus_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(usuario=request.user)
        return render(request, 'seus_pets.html', {'pets': pets, 'usuario': request.user.username})

@login_required
def remover_pet(request, id):
    pet = Pet.objects.get(id=id)

    if not pet.usuario == request.user:
        messages.add_message(request, messages.ERROR, 'Esse pet não é seu!')
    else:
        pet.delete()
        messages.add_message(request, messages.SUCCESS, 'Pet removido com sucesso.')
    
    return redirect(reverse('seus_pets'))

@login_required
def ver_pet(request, id):
    if request.method == "GET":
        pet = Pet.objects.get(id = id)
        return render(request, 'ver_pet.html', {'pet': pet, 'usuario': request.user.username})

@login_required
def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(status="AG").exclude(usuario=request.user)
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos, 'usuario': request.user.username})

@login_required
def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html', {'usuario': request.user.username})

@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()

    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).count()
        qtd_adocoes.append(adocoes)

    racas = [raca.raca for raca in racas]
    data = {'qtd_adocoes': qtd_adocoes,
            'labels': racas}

    return JsonResponse(data)
