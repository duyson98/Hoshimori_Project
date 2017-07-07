# Shit tons of codes copied from Cinderella Producers

from django.db.models import Prefetch
from django.utils.translation import ugettext_lazy as _
from magi.magicollections import AccountCollection as _AccountCollection
from magi.magicollections import MagiCollection
from magi.magicollections import UserCollection as _UserCollection

from hoshimori import forms, raw
from hoshimori.models import *

############################################################
# Account
# Override

class AccountCollection(_AccountCollection):
    class ListView(_AccountCollection.ListView):
        distinct = True
        default_ordering = '-id'
        filter_form = forms.AccountFilterForm

    class AddView(_AccountCollection.AddView):
        back_to_list_button = False

        js_files = getattr(_AccountCollection.AddView, 'js_files', []) + ['mod_account']

    class EditView(_AccountCollection.EditView):
        js_files = getattr(_AccountCollection.AddView, 'js_files', []) + ['mod_account']


############################################################
# Student

class StudentCollection(MagiCollection):
    queryset = Student.objects.all()

    title = _('Student')
    plural_title = _('Students')
    icon = 'idolized'

    class ItemView(MagiCollection.ItemView):
        template = 'studentInfo'
        js_files = ['studentInfo', ]

    class ListView(MagiCollection.ListView):
        filter_form = forms.StudentFilterForm
        staff_required = False
        show_edit_button = False
        per_line = 3
        default_ordering = 'id'
        show_relevant_fields_on_ordering = False
        ajax_pagination_callback = 'ajaxModals'
        no_result_template = 'my404card'

        def extra_context(self, context):
            request = context['request']
            if 'ordering' in request.GET:
                context['ordering'] = request.GET['ordering']
            return context

        def check_permissions(self, request, context):
            super(StudentCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise StudentCollection()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True
        form_class = forms.StudentForm

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True
        allow_delete = True
        form_class = forms.StudentForm


############################################################
# Card

class CardCollection(MagiCollection):
    queryset = Card.objects.all()

    title = _('Card')
    plural_title = _('Cards')
    icon = 'cards'

    reportable = False

    class ItemView(MagiCollection.ItemView):
        template = 'default'
        # ajax_callback = 'updateCardsAndOwnedCards'
        js_files = ['cards', 'collection']

        def extra_context(self, context):
            request = context['request']
            if request.user.is_authenticated():
                context['collection'] = 'collection' in request.GET
                if context['collection']:
                    request.user.all_accounts = request.user.accounts.all().prefetch_related(
                        Prefetch('ownedcards',
                                 queryset=OwnedCard.objects.filter(card_id=context['item'].id).order_by(
                                     '-card__i_rarity', '-evolved', 'card__student_id'), to_attr='all_owned'),
                    )
                    # Set values to avoid using select_related since we already have them
                    for account in request.user.all_accounts:
                        account.owner = request.user
                        for oc in account.get_cards():
                            oc.card = context['item']
                            oc.is_mine = True
            return context

    class ListView(MagiCollection.ListView):
        filter_form = forms.CardFilterForm
        staff_required = False
        default_ordering = 'card_type,student,i_rarity'
        full_width = True
        ajax_pagination_callback = 'updateCards'
        js_files = ['cards']

        def get_queryset(self, queryset, parameters, request):
            from hoshimori.utils import filterCards
            return filterCards(queryset, parameters, request)

        def extra_context(self, context):
            request = context['request']
            context['next'] = request.GET.get('next', None)
            context['next_title'] = request.GET.get('next_title', None)
            if context['is_last_page']:
                context['share_sentence'] = _('Check out my collection of cards!')
            if 'student' in request.GET and request.GET['student']:
                context['student'] = Student.objects.get(id=request.GET['student'])
            return context

        def check_permissions(self, request, context):
            super(CardCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise CardCollection()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True
        form_class = forms.CardForm

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True
        allow_delete = True
        form_class = forms.CardForm


############################################################
# Owned card

class OwnedCardCollection(MagiCollection):
    queryset = OwnedCard.objects.select_related('card')

    title = _('Card')
    plural_title = _('Cards')
    icon = 'album'
    navbar_link = False

    class ItemView(MagiCollection.ItemView):
        comments_enabled = False
        js_files = ['ownedcards']

    class ListView(MagiCollection.ListView):
        staff_required = False
        default_ordering = '-card__i_rarity,-evolved,card__student'
        per_line = 6
        page_size = 40
        col_break = 'xs'
        filter_form = forms.OwnedCardFilterForm
        js_files = ['ownedcards']
        ajax_pagination_callback = 'updateOwnedCards'

        def foreach_item(selfindex, item, context):
            item.is_mine = context['request'].user.id == item.cached_account.owner.id

        def check_permissions(self, request, context):
            super(OwnedCardCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise OwnedCardCollection()

    class EditView(MagiCollection.EditView):
        form_class = forms.OwnedCardEditForm
        js_files = ['edit_ownedcard']
        allow_delete = True
        back_to_list_button = False

        def redirect_after_edit(self, request, item, ajax):
            if ajax:
                if 'collection' in request.GET:
                    return '/ajax/cardcollection/{}/'.format(item.card_id)
                return '/ajax/card/{}/'.format(item.card_id)
            if 'back_to_profile' in request.GET:
                return item.account.owner.item_url
            return item.card.item_url

        def redirect_after_delete(self, request, item, ajax):
            if ajax:
                if 'collection' in request.GET:
                    return '/ajax/cardcollection/{}/'.format(item.card_id)
                return '/ajax/card/{}/'.format(item.card_id)
            if 'back_to_profile' in request.GET:
                return item.account.owner.item_url
            return item.card.item_url


############################################################
# Weapon

class WeaponCollection(MagiCollection):
    queryset = Weapon.objects.all()

    title = _('Weapon')
    plural_title = _('Weapons')
    icon = 'album'

    class ItemView(MagiCollection.ItemView):
        template = 'default'

    class ListView(MagiCollection.ListView):
        filter_form = forms.WeaponFilterForm
        staff_required = False

        def check_permissions(self, request, context):
            super(WeaponCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise WeaponCollection()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True


# class MaterialCollection(MagiCollection):
#     queryset = Material.objects.all()
#
#     title = _('Material')
#     plural_title = _('Materials')
#     icon = 'album'
#
#     class ItemView(MagiCollection.ItemView):
#         template = 'default'
#
#     class ListView(MagiCollection.ListView):
#         filter_form = forms.MaterialFilterForm
#         staff_required = False
#
#         def check_permissions(self, request, context):
#             super(MaterialCollection.ListView, self).check_permissions(request, context)
#             if request.user.username == 'bad_staff':
#                 raise MaterialCollection()
#
#     class AddView(MagiCollection.AddView):
#         staff_required = True
#         multipart = True
#
#     class EditView(MagiCollection.EditView):
#         staff_required = True
#         multipart = True


############################################################
# Stage

class StageCollection(MagiCollection):
    queryset = Stage.objects.all()

    title = _('Stage')
    plural_title = _('Stages')
    icon = 'deck'

    class ItemView(MagiCollection.ItemView):
        template = 'stage'

    class ListView(MagiCollection.ListView):
        filter_form = forms.StageFilterForm
        per_line = 4
        page_size = 20
        staff_required = False

        def check_permissions(self, request, context):
            super(StageCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise StageCollection()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True
        allow_delete = True


############################################################
# Irous

class IrousVariationCollection(MagiCollection):
    queryset = IrousVariation.objects.all()

    title = _('Irous Variation')
    plural_title = _('Irous Variations')
    icon = 'deck'
    navbar_link = False

    class ItemView(MagiCollection.ItemView):
        template = 'irousvariation'

    class ListView(MagiCollection.ListView):
        filter_form = forms.IrousVariationFilterForm
        staff_required = False
        default_ordering = 'id'

        def check_permissions(self, request, context):
            super(IrousVariationCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise IrousVariationCollection()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True
        allow_delete = True
