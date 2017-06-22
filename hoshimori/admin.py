from django.contrib import admin
from django import forms

from hoshimori.models import *


class IrousuAdminForm(forms.ModelForm):

    weak = forms.MultipleChoiceField(choices=WEAPON_CHOICES, widget=forms.CheckboxSelectMultiple())

    def clean_weak(self):
        return self.cleaned_data["weak"]

    strong = forms.MultipleChoiceField(choices=WEAPON_CHOICES, widget=forms.CheckboxSelectMultiple())

    def clean_strong(self):
        return self.cleaned_data["strong"]

    guard = forms.MultipleChoiceField(choices=WEAPON_CHOICES, widget=forms.CheckboxSelectMultiple())

    def clean_guard(self):
        return self.cleaned_data["guard"]


class IrousuAdmin(admin.ModelAdmin):
    form = IrousuAdminForm


admin.site.register(Account)
admin.site.register(OwnedCard)
admin.site.register(FavoriteCard)
admin.site.register(Student)
admin.site.register(Card)
admin.site.register(ActionSkillEffect)
admin.site.register(ActionSkill)
admin.site.register(Weapon)
admin.site.register(WeaponUpgrade)
admin.site.register(WeaponEffect)
admin.site.register(Stage)
admin.site.register(StageDifficulty)
admin.site.register(Nakayoshi)
admin.site.register(Irousu, IrousuAdmin)
admin.site.register(IrousuVariation)
