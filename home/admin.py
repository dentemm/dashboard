from django.contrib import admin

from .models import EventPage, Task, Request

@admin.register(EventPage)
class EventPageAdmin(admin.ModelAdmin):
	pass

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	pass

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
	pass

