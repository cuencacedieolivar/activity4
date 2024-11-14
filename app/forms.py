from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Plant, HealthStatus, CareLog, Reminder, WateringSchedule
from django.forms import DateInput

# User Registration Form with Email
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Login Form with Email and Password
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


# Form for Adding or Updating Plant Details, Including Image
class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'type', 'care_instructions', 'image', 'visibility']  # Include all fields from the Plant model



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
        fields = ['task', 'reminder_time', 'is_completed']  # Including is_completed field for marking reminders complete



class WateringScheduleForm(forms.ModelForm):
    class Meta:
        model = WateringSchedule
        fields = ['water_frequency', 'last_watered', 'next_watering']
        widgets = {
            'last_watered': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_watering': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }