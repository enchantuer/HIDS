from django.contrib import admin

from dashboard.models import Agent, Alert

# Register your models here.
admin.site.register(Agent)
admin.site.register(Alert)
