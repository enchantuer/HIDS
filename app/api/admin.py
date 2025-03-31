from django.contrib import admin

from api.models import Agent, Alert, LogNbRequest

# Register your models here.
admin.site.register(Agent)
admin.site.register(Alert)
admin.site.register(LogNbRequest)