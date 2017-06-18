from web.magicollections import MagiCollection
from hoshimori import models
from django.utils.translation import ugettext_lazy as _

class StudentCollection(MagiCollection):
    queryset = models.Student.objects.all()

    title = _('Student')
    plural_title = _('Students')

    class ListView(MagiCollection.ListView):
        staff_required = True

        def check_permissions(self, request, context):
            super(StudentCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise StudentCollection()

class MaterialCollection(MagiCollection):
    queryset = models.Material.objects.all()

    title = _('Material')
    plural_title = _('Materials')

    class ListView(MagiCollection.ListView):
        staff_required = True

        def check_permissions(self, request, context):
            super(MaterialCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise StudentCollection()

class CardCollection(MagiCollection):
    queryset = models.Material.objects.all()

    title = _('Card')
    plural_title = _('Cards')

    class ListView(MagiCollection.ListView):
        staff_required = True

        def check_permissions(self, request, context):
            super(CardCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise StudentCollection()

class WeaponCollection(MagiCollection):
    queryset = models.Material.objects.all()

    title = _('Weapon')
    plural_title = _('Weapons')

    class ListView(MagiCollection.ListView):
        staff_required = True

        def check_permissions(self, request, context):
            super(WeaponCollection.ListView, self).check_permissions(request, context)
            if request.user.username == 'bad_staff':
                raise StudentCollection()
