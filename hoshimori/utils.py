import sys
from magi.utils import globalContext as magi_globalContext

from hoshimori import models

##################################################
def debug_message(msg):
    print >> sys.stderr, msg
##################################################


def globalContext(request):
    context = magi_globalContext(request)
    return context


def onUserEdited(request):
    accounts = models.Account.objects.filter(owner_id=request.user.id).select_related('owner', 'owner__preferences')
    for account in accounts:
        account.force_cache_owner()


def onPreferencesEdited(request):
    accounts = models.Account.objects.filter(owner_id=request.user.id).select_related('owner', 'owner__preferences')
    for account in accounts:
        account.force_cache_owner()


def filterCards(queryset, parameters, request):
    if request.user.is_authenticated():
        request.user.all_accounts = request.user.accounts.all()
        accounts_pks = ','.join([str(account.pk) for account in request.user.all_accounts])
        if accounts_pks:
            queryset = queryset.extra(select={
                'total_owned': 'SELECT COUNT(*) FROM hoshimori_ownedcard WHERE card_id = hoshimori_card.id AND account_id IN ({})'.format(
                    accounts_pks),
            })
    return queryset
