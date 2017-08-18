# Create your views here.

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from magi.utils import globalContext as web_globalContext, ajaxContext

from hoshimori.magicollections import CardCollection
from hoshimori.models import *
from hoshimori.utils import item_view, filterCards


def globalContext(request):
    context = web_globalContext(request)
    return context


def cardstat(request, card):
    context = ajaxContext(request)
    context['card'] = get_object_or_404(Card, pk=card)
    return render(request, 'include/cards-stats.html', context)


def addcard(request, card):
    if request.method != "POST":
        raise PermissionDenied()
    collection = 'collection' in request.GET
    queryset = Card
    if not collection:
        # Note: calling filterCards will add extra info need to display the card
        queryset = filterCards(Card.objects.all(), {}, request)
    card = get_object_or_404(queryset, pk=card)
    account = get_object_or_404(Account, pk=request.POST.get('account', None), owner=request.user)
    OwnedCard.objects.create(card=card, account=account, evolved=card.evolvable, level=card.max_level)
    OwnedCard.objects.get(card=card, account=account).force_cache_stats()
    if not collection:
        card.total_owned += 1
    if collection:
        return cardcollection(request, card.id)
    else:
        context = web_globalContext(request)
        return item_view(request, context, 'card', CardCollection, pk=card.id, item=card, ajax=True)


def cardcollection(request, card):
    context = web_globalContext(request)
    collection = CardCollection
    request.GET = request.GET.copy()
    request.GET['collection'] = True
    return item_view(request, context, 'card', collection, item_template='../include/cards-collection', pk=card,
                     ajax=True)


def account_about(request, account):
    context = ajaxContext(request)
    context['account'] = get_object_or_404(Account.objects.all(), pk=account)
    return render(request, 'ajax/account_about.html', context)


def account_builder(request, account):
    context = ajaxContext(request)
    context['account'] = get_object_or_404(Account.objects.all(), pk=account)
    context['ownedcards'] = OwnedCard.objects.filter(account=account).order_by("-card__id")
    import json
    oc_dict = {}
    for oc in context['ownedcards']:
        card = oc.card
        oc_dict[card.id] = {
            "card-chara": card.student.id,
            "evolved": oc.evolved,
            "subcard-effect": card.subcard_effect,
            "hp": oc._cache_hp,
            "sp": oc._cache_sp,
            "atk": oc._cache_atk,
            "def": oc._cache_def,
            "nakayoshi-jpn-name": card.japanese_nakayoshi_title,
            "nakayoshi-effect": card.evolved_nakayoshi_skill_effect if oc.evolved else card.nakayoshi_skill_effect,
            "nakayoshi-target": card.evolved_nakayoshi_skill_target if oc.evolved else card.nakayoshi_skill_target,
            "skill-jpn-name": card.japanese_skill_name,
            "skill-combo": card.evolved_action_skill_combo if oc.evolved else card.action_skill_combo,
            "skill-sp": card.skill_SP,
            "skill-effect": card.action_skill_effects,
            "skill-affinity": card.skill_affinity,
        }
    context['jsonoc'] = json.dumps(oc_dict)
    context['weapontypes'] = WEAPON_DICT
    return render(request, 'ajax/account_builder.html', context)
