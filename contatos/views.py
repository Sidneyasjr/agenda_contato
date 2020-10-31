from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.db.models import Q, Value
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from .models import Contato, Categoria
from django.core.paginator import Paginator
from django.db.models.functions import Concat
from django.contrib import messages


@login_required(redirect_field_name='login')
def agenda(request):
    contatos = Contato.objects.filter(mostrar=True).order_by('nome')
    paginator = Paginator(contatos, 10)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/agenda.html', {
        'contatos': contatos
    })


@login_required(redirect_field_name='login')
def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if not contato.mostrar:
        raise Http404()
    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })


@login_required(redirect_field_name='login')
def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(request, messages.ERROR, 'A busca está vazia')
        return redirect('agenda')

    campos = Concat('nome', Value(' '), 'sobrenome')
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(nome_completo__icontains=termo, mostrar=True)

    paginator = Paginator(contatos, 10)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })


@login_required(redirect_field_name='login')
def novo_contato(request):
    categorias = Categoria.objects.all()
    if request.method != 'POST':
        return render(request, 'contatos/novo_contato.html', {'categorias': categorias, })

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    telefone = request.POST.get('telefone')
    email = request.POST.get('email')
    categoria = request.POST.get('categoria')
    foto = request.POST.get('foto')
    descricao = request.POST.get('descricao')

    if not nome or not sobrenome or not telefone or not categoria:
        messages.error(request, 'Preencha os campos obrigatorios')
        return render(request, 'contatos/novo_contato.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email invalido')
        return render(request, 'contatos/novo_contato.html')

    messages.success(request, 'Usuario cadastrado com sucesso')
    contato = Contato.objects.create(
        nome=nome,
        sobrenome=sobrenome,
        telefone=telefone,
        email=email,
        categoria=categoria,
        foto=foto,
        descricao=descricao,
    )
    print(contato)
    contato.save()
    return redirect('agenda')
