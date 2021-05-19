from django.contrib import admin
from django import forms

from .models import Tenant, Upstream


PASSWORD_PLACEHOLDER = '*' * 16


admin.site.register(Tenant)


class UpstreamForm(forms.ModelForm):
    class Meta:
        model = Upstream
        fields = '__all__'
        widgets = {
            '_password': forms.PasswordInput(render_value=True),
        }


@admin.register(Upstream)
class UpstreamAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tenant')
    list_filter = ('tenant__name',)
    list_select_related = ('tenant',)
    search_fields = ['short_name']
    form = UpstreamForm

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field)
        if obj:
            obj._password = PASSWORD_PLACEHOLDER
        return obj

    def save_model(self, request, obj, form, change):
        if obj._password != PASSWORD_PLACEHOLDER:
            obj.password = obj._password  # Encrypt password before saving
        return super().save_model(request, obj, form, change)
