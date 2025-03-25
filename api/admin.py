from django.contrib import admin

from api.models import Agent, Alert

# Register your models here.
admin.site.register(Agent)
admin.site.register(Alert)