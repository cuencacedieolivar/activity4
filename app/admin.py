from django.contrib import admin
from .models import Plant, HealthStatus, CustomUser, CareLog, Reminder, WateringSchedule

admin.site.register(Plant)
admin.site.register(HealthStatus)
admin.site.register(CustomUser)
admin.site.register(CareLog)
admin.site.register(Reminder)
admin.site.register(WateringSchedule)
