from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _, string_concat
from web.magicollections import MagiCollection

from hoshimori import forms
from hoshimori import models


############################################################
# Student

class StudentCollection(MagiCollection):
    queryset = models.Student.objects.all()

    title = _('Student')
    plural_title = _('Students')
    icon = 'id'

    def to_fields(self, item, *args, **kwargs):
        fields = super(StudentCollection, self).to_fields(item, *args, icons={
            'unlock': 'perfectlock',
            'name': 'id',
            'japanese_name': 'id',
            'description': 'id',
            'school_year': 'max-bond',
            'birthday': 'event',
            'star_sign': 'hp',
            'blood_type': 'hp',
            'extra_activity': 'activities',
            'catchphrase_1': 'comments',
            'catchphrase_2': 'comments',
            'catchphrase_3': 'comments',
            'hobby_1': 'star',
            'hobby_2': 'star',
            'hobby_3': 'star',
            'food_likes': 'heart',
            'food_dislikes': 'heart-empty',
            'family': 'users',
            'dream': 'idolized',
            'ideal_1': 'heart',
            'ideal_2': 'heart',
            'ideal_3': 'heart',
            'pastime': 'star',
            'destress': 'star',
            'fav_memory': 'event',
            'fav_phrase': 'comments',
            'secret': 'perfectlock',
            'CV': 'profile',
            'romaji_CV': 'profile',
        }, **kwargs)
        return fields

    class ItemView(MagiCollection.ItemView):
        template = 'default'

    class ListView(MagiCollection.ListView):
        filter_form = forms.StudentFilterForm
        staff_required = False

        def check_permissions(self, request, context):
            super(StudentCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise StudentCollection()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True


############################################################
# Card

class CardCollection(MagiCollection):
    queryset = models.Card.objects.all()

    title = _('Card')
    plural_title = _('Cards')
    icon = 'deck'

    class ItemView(MagiCollection.ItemView):
        template = 'default'

    class ListView(MagiCollection.ListView):
        filter_form = forms.CardFilterForm
        staff_required = False

        def check_permissions(self, request, context):
            super(CardCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise CardCollection()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True


############################################################
# Weapon

class WeaponCollection(MagiCollection):
    queryset = models.Weapon.objects.all()

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
#     queryset = models.Material.objects.all()
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
# Owned card

class OwnedCardCollection(MagiCollection):
    queryset = models.OwnedCard.objects.select_related('card')

    title = _('Card')
    plural_title = _('Cards')
    icon = 'album'
    navbar_link = False

    class ListView(MagiCollection.ListView):
        staff_required = False
        default_ordering = '-card__i_rarity'
        per_line = 6
        page_size = 40

        def check_permissions(self, request, context):
            super(OwnedCardCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise OwnedCardCollection()

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True

############################################################
# Stage

class StageCollection(MagiCollection):
    queryset = models.Stage.objects.all()

    title = _('Stage')
    plural_title = _('Stages')
    icon = 'deck'

    class ItemView(MagiCollection.ItemView):
        template = 'default'

    class ListView(MagiCollection.ListView):
        filter_form = forms.StageFilterForm
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

############################################################
# Irousu

class IrousuVariationCollection(MagiCollection):
    queryset = models.IrousuVariation.objects.all()

    title = _('Irousu Variation')
    plural_title = _('Irousu Variations')
    icon = 'deck'

    class ItemView(MagiCollection.ItemView):
        enabled = False

    class ListView(MagiCollection.ListView):
        filter_form = forms.IrousuVariationFilterForm
        staff_required = False
        default_ordering = 'id'

        def check_permissions(self, request, context):
            super(IrousuVariationCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise IrousuVariationCollection()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True



