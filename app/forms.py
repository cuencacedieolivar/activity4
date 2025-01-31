from django import forms
from .models import Plant, HealthStatus, CareLog, Reminder, WateringSchedule
from django.forms import DateInput, TimeInput





# Form for Adding or Updating Plant Details, Including Image
class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'type', 'care_instructions', 'image']  # Include all fields from the Plant model



class HealthStatusForm(forms.ModelForm):
    class Meta:
        model = HealthStatus
        fields = ['status', 'notes']  # Exclude auto-generated update_time field


# Form for Logging Plant Care Activities
class CareLogForm(forms.ModelForm):
    class Meta:
        model = CareLog
        fields = ['action', 'notes']  # Fields aligned with the CareLog model


# Form for Setting Plant Care Reminders
class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['task', 'reminder_time', 'is_completed']
        widgets = {
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }


class WateringScheduleForm(forms.ModelForm):
    class Meta:
        model = WateringSchedule
        fields = ['water_frequency', 'last_watered', 'next_watering']
        widgets = {
            'last_watered': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_watering': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

