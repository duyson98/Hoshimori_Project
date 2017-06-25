# Create your views here.
from copy import copy

import sys

from django.http import HttpResponse
from magi.views_collections import *

from hoshimori.magicollections import CardCollection
from hoshimori.models import *


# TODO: Proper redirect
def addcard(request, card):
    if request.method != "POST":
        raise PermissionDenied()
    collection = 'collection' in request.GET
    queryset = Card.objects.all()
    if not collection:
        from hoshimori.utils import filterCards
        queryset = filterCards(queryset, {}, request)
    card = get_object_or_404(queryset, pk=card)
    account = get_object_or_404(Account, pk=request.POST.get('account', None), owner=request.user)
    OwnedCard.objects.create(card=card, account=account)
    if not collection:
        card.total_owned += 1
    if collection:
        return cardcollection(request, card.id)
    else:
        # return item_view(request, 'card', CardCollection, pk=card.id, item=card, ajax=True)
        return HttpResponse('Card added! Good for you')

# TODO: Proper redirect
def cardcollection(request, card):
    collection = CardCollection
    # collection['item'] = collection['item'].copy()
    collection.ItemView = copy(collection.ItemView)
    request.GET = request.GET.copy()
    request.GET['collection'] = True
    collection.ItemView.template = '../include/cards-collection'
    # return item_view(request, 'card', collection, pk=card, ajax=True)
    return HttpResponse('No prob here')