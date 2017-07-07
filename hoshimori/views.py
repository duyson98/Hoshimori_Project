# Create your views here.
from copy import copy
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from magi.utils import globalContext as web_globalContext

from hoshimori.magicollections import CardCollection
from hoshimori.models import *
from hoshimori.utils import item_view, filterCards


def globalContext(request):
    context = web_globalContext(request)
    context['something'] = 'something'
    return context


# TODO: Proper redirect
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
    OwnedCard.objects.create(card=card, account=account)
    if not collection:
        card.total_owned += 1
    if collection:
        return cardcollection(request, card.id)
    else:
        context = web_globalContext(request)
        return item_view(request, context, 'card', CardCollection, pk=card.id, item=card, ajax=True)


# TODO: Proper redirect
def cardcollection(request, card):
    context = web_globalContext(request)
    collection = copy(CardCollection)
    request.GET = request.GET.copy()
    request.GET['collection'] = True
    collection.ItemView.template = '../include/cards-collection'
    return item_view(request, context, 'card', collection, pk=card, ajax=True)
