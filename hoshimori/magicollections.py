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