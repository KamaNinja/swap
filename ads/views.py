from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm, FilterProposalForm
from .filters import build_proposal_filters
from .utils import get_ads_context


def index(request):
    context = get_ads_context(request)
    return render(request, 'ads/index.html', context)


@login_required
def my_ads(request):
    context = get_ads_context(request, user_specific=True)
    return render(request, 'ads/index.html', context)


def ad_details(request, ad_pk):
    ad = get_object_or_404(Ad, pk=ad_pk)
    return render(request, 'ads/ad_details.html', {'ad': ad})


@login_required
def add_ad(request):
    form = AdForm(request.POST or None, request.FILES)

    if request.method == 'POST' and form.is_valid():
        ad = form.save(commit=False)
        ad.user = request.user
        ad.save()
        messages.success(request, 'Объявление успешно добавлено.')
        return redirect(ad.get_absolute_url())

    return render(request, 'ads/add_ad.html', {'form': form})


@login_required
def update_ad(request, ad_pk):
    ad = get_object_or_404(Ad, pk=ad_pk, user=request.user)
    form = AdForm(request.POST or None, instance=ad)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Объявление успешно обновлено.')
        return redirect(ad.get_absolute_url())

    return render(request, 'ads/update_ad.html', {'form': form})


@login_required
def delete_ad(request, ad_pk):
    ad = get_object_or_404(Ad, pk=ad_pk, user=request.user)
    ad.delete()
    messages.success(request, 'Объявление успешно удалено.')
    return redirect('home')


@login_required
def my_proposals(request):
    form = FilterProposalForm(request.GET or None)
    filters = build_proposal_filters(request)
    selected_status = request.GET.getlist('status')

    common_related = ['ad_sender', 'ad_sender__user', 'ad_receiver', 'ad_receiver__user']

    outgoing = ExchangeProposal.objects.filter(
        ad_sender__user=request.user
    ).filter(filters).select_related(*common_related)

    incoming = ExchangeProposal.objects.filter(
        ad_receiver__user=request.user
    ).filter(filters).select_related(*common_related)

    context = {
        'form': form,
        'incoming': incoming,
        'outgoing': outgoing,
        'selected_status': selected_status
    }
    return render(request, 'ads/my_proposals.html', context)


@login_required
def proposal_details(request, proposal_pk):
    proposal = get_object_or_404(
        ExchangeProposal.objects.select_related(
            'ad_sender', 'ad_sender__user',
            'ad_receiver', 'ad_receiver__user'
        ),
        pk=proposal_pk
    )
    return render(request, 'ads/proposal_details.html', {'proposal': proposal})


@login_required
def suggest_exchange(request, ad_pk):
    ad = get_object_or_404(Ad, pk=ad_pk)
    form = ExchangeProposalForm(request.POST or None, user=request.user, initial={'ad_receiver': ad})

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Предложение успешно отправлено.')
        return redirect(ad.get_absolute_url())

    return render(request, 'ads/suggest_exchange.html', {'form':  form})


@login_required
def exchange_action(request, proposal_pk):
    proposal = get_object_or_404(ExchangeProposal, pk=proposal_pk)

    if proposal.ad_receiver.user != request.user:
        messages.error(request, 'У вас нет прав для изменения этого предложения.')
        return redirect('my_proposals')

    action = request.POST.get('action')
    if action == 'accept':
        proposal.status = 'accepted'
        messages.success(request, 'Вы приняли предложение обмена.')
    elif action == 'reject':
        proposal.status = 'rejected'
        messages.success(request, 'Вы отклонили предложение обмена.')
    else:
        messages.error(request, 'Неверное действие.')

    proposal.save()
    return redirect('my_proposals')
