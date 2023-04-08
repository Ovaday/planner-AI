from django.contrib import admin
from service_routine.models import ServiceM, ServiceMAdmin

# Register your models here.
admin.site.register(ServiceM, ServiceMAdmin)