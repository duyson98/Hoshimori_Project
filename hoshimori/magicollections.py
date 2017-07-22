# Shit tons of codes copied from Cinderella Producers
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.utils.translation import ugettext_lazy as _
from magi.magicollections import AccountCollection as _AccountCollection
from magi.magicollections import MagiCollection
from magi.magicollections import UserCollection as _UserCollection
from magi.utils import CuteFormType, getMagiCollection, ordinalNumber

from hoshimori import forms, raw
from hoshimori.models import *


############################################################
# User
# Override
class UserCollection(_UserCollection):
    icon = 'heart'

    class ItemView(MagiCollection.ItemView):
        js_files = ['profile', 'profile_account_tabs', 'cards']
        template = 'profile'
        comments_enabled = False
        show_edit_button = False
        ajax = False
        shortcut_urls = [
            ('me', 'me'),
        ]

        def get_item(self, request, pk):
            if pk == 'me':
                if request.user.is_authenticated():
                    pk = request.user.id
                else:
                    from magi.middleware.httpredirect import HttpRedirectException
                    raise HttpRedirectException('/signup/')
            return {'pk': pk}

        def reverse_url(self, text):
            return {
                'username': text,
            }

        def get_queryset(self, queryset, parameters, request):
            if request.user.is_authenticated():
                queryset = queryset.extra(select={
                    'followed': 'SELECT COUNT(*) FROM magi_userpreferences_following WHERE userpreferences_id = {} AND user_id = auth_user.id'.format(
                        request.user.preferences.id),
                })
                queryset = queryset.extra(select={
                    'is_followed_by': 'SELECT COUNT(*) FROM magi_userpreferences_following WHERE userpreferences_id = (SELECT id FROM magi_userpreferences WHERE user_id = auth_user.id) AND user_id = {}'.format(
                        request.user.id),
                })
            queryset = queryset.extra(select={
                'total_following': 'SELECT COUNT(*) FROM magi_userpreferences_following WHERE userpreferences_id = (SELECT id FROM magi_userpreferences WHERE user_id = auth_user.id)',
                'total_followers': 'SELECT COUNT(*) FROM magi_userpreferences_following WHERE user_id = auth_user.id',
            })
            queryset = queryset.select_related('preferences', 'favorite_character1', 'favorite_character2',
                                               'favorite_character3')
            from django.db.models import Prefetch
            from magi.models import UserLink
            queryset = queryset.prefetch_related(Prefetch('accounts', to_attr='all_accounts'),
                                                 Prefetch('links', queryset=UserLink.objects.order_by('-i_relevance'),
                                                          to_attr='all_links'))
            return queryset

        def extra_context(self, context):
            user = context['item']
            request = context['request']
            context['is_me'] = user.id == request.user.id

            # Badges
            if 'badge' in context['all_enabled']:
                context['item'].latest_badges = list(
                    context['item'].badges.filter(show_on_top_profile=True).order_by('-date', '-id')[:6])
                if len(context['item'].latest_badges) == 6:
                    context['more_badges'] = True
                context['item'].latest_badges = context['item'].latest_badges[:5]

            # Profile tabs
            from magi.settings import SHOW_TOTAL_ACCOUNTS
            context['show_total_accounts'] = SHOW_TOTAL_ACCOUNTS
            from magi.settings import PROFILE_TABS
            context['profile_tabs'] = PROFILE_TABS
            context['profile_tabs_size'] = 100 / len(context['profile_tabs'])
            context['opened_tab'] = context['profile_tabs'].keys()[0]
            if 'open' in request.GET and request.GET['open'] in context['profile_tabs']:
                context['opened_tab'] = request.GET['open']

            # Links
            context['item'].all_links = list(context['item'].all_links)
            meta_links = []
            from magi.settings import FAVORITE_CHARACTERS
            if FAVORITE_CHARACTERS:
                for i in range(1, 4):
                    if getattr(user.preferences, 'favorite_character{}'.format(i)):
                        from magi.settings import FAVORITE_CHARACTER_NAME
                        link = AttrDict({
                            'type': (_(FAVORITE_CHARACTER_NAME) if FAVORITE_CHARACTER_NAME else _(
                                '{nth} Favorite Character')).format(nth=_(ordinalNumber(i))),
                            # May be used by FAVORITE_CHARACTER_TO_URL
                            'raw_value': getattr(user.preferences, 'favorite_character{}'.format(i)),
                            'value': user.preferences.localized_favorite_character(i),
                            'translate_type': False,
                            'image_url': user.preferences.favorite_character_image(i),
                        })
                        from magi.settings import FAVORITE_CHARACTER_TO_URL
                        link.url = FAVORITE_CHARACTER_TO_URL(link)
                        meta_links.append(AttrDict(link))
            if user.preferences.location:
                latlong = '{},{}'.format(user.preferences.latitude,
                                         user.preferences.longitude) if user.preferences.latitude else None
                link = AttrDict({
                    'type': 'Location',
                    'value': user.preferences.location,
                    'translate_type': True,
                    'flaticon': 'world',
                    'url': u'/map/?center={}&zoom=10'.format(latlong) if 'map' in context[
                        'all_enabled'] and latlong else u'https://www.google.com/maps?q={}'.format(
                        user.preferences.location),
                })
                meta_links.append(link)
            if user.preferences.birthdate:
                today = datetime.date.today()
                birthday = user.preferences.birthdate.replace(year=today.year)
                if birthday < today:
                    birthday = birthday.replace(year=today.year + 1)
                from django.utils import dateformat
                meta_links.append(AttrDict({
                    'type': 'Birthdate',
                    'value': u'{} ({})'.format(user.preferences.birthdate,
                                               _(u'{age} years old').format(age=user.preferences.age)),
                    'translate_type': True,
                    'flaticon': 'event',
                    'url': 'https://www.timeanddate.com/countdown/birthday?iso={date}T00&msg={username}%27s+birthday'.format(
                        date=dateformat.format(birthday, "Ymd"), username=user.username),
                }))
            context['item'].all_links = meta_links + context['item'].all_links
            num_links = len(context['item'].all_links)
            best_links_on_last_line = 0
            for i in range(4, 7):
                links_on_last_line = num_links % i
                if links_on_last_line == 0:
                    context['per_line'] = i
                    break
                if links_on_last_line > best_links_on_last_line:
                    best_links_on_last_line = links_on_last_line
                    context['per_line'] = i

            # Javascript sentences
            context['add_activity_sentence'] = _('Share your adventures!')
            activity_collection = getMagiCollection('activity')
            if 'activity' in context['all_enabled']:
                context['add_activity_sentence'] = activity_collection.list_view.add_button_subtitle
            context['share_sentence'] = _('Check out {username}\'s awesome collection!').format(
                username=context['item'].username)
            context['share_url'] = context['item'].http_item_url

            for account in context['item'].all_accounts:
                show = request.GET.get('account{}'.format(account.id), 'Cards')
                account.show = show if show in raw.ACCOUNT_TABS_LIST else 'Cards'
            context['account_tabs'] = raw.ACCOUNT_TABS
            return context


############################################################
# Account
# Override


class AccountCollection(_AccountCollection):
    class ListView(_AccountCollection.ListView):
        distinct = True
        default_ordering = '-id'
        filter_form = forms.AccountFilterForm

        filter_cuteform = {
            'i_os': {
                'image_folder': 'os_logos'
            },
        }

        def get_queryset(self, queryset, parameters, request):
            if 'own_card' in parameters and parameters['own_card']:
                queryset = queryset.filter(ownedcards__card__id=parameters['own_card'])
            return queryset

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

    filter_cuteform = {
        'i_school_year': {
            'image_folder': 'i_school_year',
            'to_cuteform': 'value',
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'i_blood_type': {
            'type': CuteFormType.HTML,
        },
        'i_star_sign': {
            'image_folder': 'i_star_sign'
        }
    }

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
        no_result_template = 'empty_query'

        def extra_context(self, context):
            request = context['request']
            if 'ordering' in request.GET:
                context['ordering'] = request.GET['ordering']
            return context

        def check_permissions(self, request, context):
            super(StudentCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise PermissionDenied()

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

    filter_cuteform = {
        'student': {
            'image_folder': 'thumb_students',
            'to_cuteform': 'value',
            'extra_settings': {
                'modal': 'true',
                'modal-text': 'true',
            },
        },
        'i_card_type': {
            'type': CuteFormType.HTML,
        },
        'i_rarity': {
            'type': CuteFormType.HTML,
        },
        'i_weapon': {
            'image_folder': 'i_weapon'
        }
    }

    class ItemView(MagiCollection.ItemView):
        template = 'cardInfo'
        ajax_callback = 'updateCardsAndOwnedCards'
        js_files = ['cards', 'collection']

        def extra_context(self, context):
            request = context['request']
            if request.user.is_authenticated():
                context['collection'] = 'collection' in request.GET
                if context['collection']:
                    request.user.all_accounts = request.user.accounts.all().prefetch_related(
                        Prefetch('ownedcards',
                                 queryset=OwnedCard.objects.filter(card_id=context['item'].id).order_by('-card__i_rarity', 'card__student_id'), to_attr='all_owned'),
                    )
                    # Set values to avoid using select_related since we already have them
                    for account in request.user.all_accounts:
                        account.owner = request.user
                        for oc in account.all_owned:
                            oc.card = context['item']
                            oc.is_mine = True
            return context

    class ListView(MagiCollection.ListView):
        filter_form = forms.CardFilterForm
        staff_required = False
        default_ordering = 'i_card_type,student,i_rarity'
        full_width = True
        ajax_pagination_callback = 'updateCards'
        js_files = ['cards']
        no_result_template = 'empty_query'

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
                raise PermissionDenied()

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
        no_result_template = 'empty_query'

        def foreach_item(self, index, item, context):
            item.is_mine = context['request'].user.id == item.cached_account.owner.id

        def check_permissions(self, request, context):
            super(OwnedCardCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise PermissionDenied()

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

    filter_cuteform = {
        'i_type': {
            'image_folder': 'i_weapon'
        }
    }

    class ItemView(MagiCollection.ItemView):
        template = 'default'

    class ListView(MagiCollection.ListView):
        filter_form = forms.WeaponFilterForm
        staff_required = False
        no_result_template = 'empty_query'

        def check_permissions(self, request, context):
            super(WeaponCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise PermissionDenied()

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
#                 raise PermissionDenied()
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
        no_result_template = 'empty_query'

        def check_permissions(self, request, context):
            super(StageCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise PermissionDenied()

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
        no_result_template = 'empty_query'

        def check_permissions(self, request, context):
            super(IrousVariationCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise PermissionDenied()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True
        allow_delete = True
