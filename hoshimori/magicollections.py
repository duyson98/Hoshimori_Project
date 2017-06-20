from web.magicollections import MagiCollection
from hoshimori import models
from django.utils.translation import ugettext_lazy as _

from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.utils.formats import dateformat
from django.utils.safestring import mark_safe
from web.utils import setSubField, CuteFormType, CuteFormTransform, FAVORITE_CHARACTERS_IMAGES, getMagiCollection, torfc2822
from web.default_settings import RAW_CONTEXT
from hoshimori import forms


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
            'blood_type': 'hp',
            'extra_activity': 'activities',
            'food_likes': 'heart',
            'food_dislikes': 'heart-empty',
            'hobby_1': 'star',
            'hobby_2': 'star',
            'hobby_3': 'star',
            'ideal_1': 'heart',
            'ideal_2': 'heart',
            'ideal_3': 'heart',
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

class CardCollection(MagiCollection):
    queryset = models.Card.objects.all()

    title = _('Card')
    plural_title = _('Cards')
    icon = 'cards'

    class ItemView(MagiCollection.ItemView):
        template = 'default'
        top_illustration = 'items/cardItem'
        ajax_callback = 'loadCard'

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

class WeaponCollection(MagiCollection):
    queryset = models.Weapon.objects.all()

    title = _('Weapon')
    plural_title = _('Weapons')

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

class MaterialCollection(MagiCollection):
    queryset = models.Material.objects.all()

    title = _('Material')
    plural_title = _('Materials')

    class ItemView(MagiCollection.ItemView):
        template = 'default'

    class ListView(MagiCollection.ListView):
        filter_form = forms.MaterialFilterForm
        staff_required = False

        def check_permissions(self, request, context):
            super(MaterialCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise MaterialCollection()

    class AddView(MagiCollection.AddView):
        staff_required = True
        multipart = True

    class EditView(MagiCollection.EditView):
        staff_required = True
        multipart = True