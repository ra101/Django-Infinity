from django.contrib import admin

from . import models


admin.site.register(models.ExampleForTenant2, admin.ModelAdmin)
