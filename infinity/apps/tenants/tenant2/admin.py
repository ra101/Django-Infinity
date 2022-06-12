from django.contrib import admin

from . import models


admin.site.register(models.ModelForTenant2, admin.ModelAdmin)
