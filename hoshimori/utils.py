import sys

from django.shortcuts import get_object_or_404, render

from hoshimori import models


##################################################

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


def item_view(request, context, name, collection, pk=None, reverse=None, ajax=False, item=None, extra_filters={},
              shortcut_url=None, item_template=None, **kwargs):
    """
    Either pk or reverse required.
    """
    item_view = collection.ItemView(collection())
    collection = collection()
    item_view.check_permissions(request, context)
    from magi.views_collections import _get_filters
    queryset = item_view.get_queryset(collection.queryset, _get_filters(request.GET, extra_filters), request)
    if not pk and reverse:
        options = item_view.reverse_url(reverse)
    else:
        options = item_view.get_item(request, pk)
    context['item'] = get_object_or_404(queryset, pk=options['pk']) if not item else item
    item_view.check_owner_permissions(request, context, context['item'])
    if shortcut_url is not None:
        context['shortcut_url'] = shortcut_url
    context['ajax'] = ajax
    context['name'] = name
    context['page_title'] = u'{title}: {item}'.format(title=collection.title, item=context['item'])
    context['js_files'] = item_view.js_files
    context['reportable'] = collection.reportable
    from magi.views_collections import _get_share_image
    context['share_image'] = _get_share_image(context, item_view, item=context['item'])
    context['comments_enabled'] = item_view.comments_enabled
    if item_template is None:
        context['item_template'] = item_view.template
    else:
        context['item_template'] = item_template
    if context['item_template'] == 'default':
        context['show_edit_button'] = False
        context['item_fields'] = collection.to_fields(context['item'])
        context['top_illustration'] = item_view.top_illustration
    context['include_below_item'] = context.get('show_edit_button', False)
    context['ajax_callback'] = item_view.ajax_callback
    item_view.extra_context(context)
    if ajax:
        context['include_template'] = 'items/{}'.format(context['item_template'])
        return render(request, 'ajax.html', context)
    return render(request, 'collections/item_view.html', context)
