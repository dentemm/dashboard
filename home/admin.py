from django.contrib import admin

from .models import UtilityStatus

@admin.register(UtilityStatus)
class UtilityStatusAdmin(admin.ModelAdmin):
	pass
