from django.contrib import admin

from .models import ModelForTenantShared


admin.site.register(ModelForTenantShared, admin.ModelAdmin)
