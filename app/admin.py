from django.contrib import admin
from .models import Plant, HealthStatus, CareLog, Reminder, WateringSchedule

admin.site.register(Plant)
admin.site.register(HealthStatus)
admin.site.register(CareLog)
admin.site.register(Reminder)
admin.site.register(WateringSchedule)
