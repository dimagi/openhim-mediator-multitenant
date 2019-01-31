from django.contrib import admin

from tenants.models import Tenant, Upstream


admin.site.register(Tenant)
admin.site.register(Upstream)
