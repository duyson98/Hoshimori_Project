# Create your views here.
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from hoshimori.models import *


def addcard(request, card):
    if request.method != "POST":
        raise PermissionDenied()
    card = get_object_or_404(Card.objects.all(), pk=card)
    account = get_object_or_404(request.user.accounts, pk=1)
    if len(OwnedCard.objects.filter(card=card, account=account)) == 0:
        OwnedCard.objects.create(card=card, account=account)
    return HttpResponseRedirect('/cards')