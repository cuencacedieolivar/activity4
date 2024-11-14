from django.urls import reverse_lazy, reverse
from .models import Plant, HealthStatus, CareLog, Reminder, WateringSchedule
from django.views import View
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import redirect, get_object_or_404 , render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, HealthStatusForm, CareLogForm, ReminderForm, WateringScheduleForm , PlantForm
from django.db.models import Q




import logging

logger = logging.getLogger(__name__)



class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm  # Use your custom form
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login page after logout

class HomePageView(TemplateView):
    template_name = 'app/home.html'  # Create this template to display products

class PlantListView(ListView):
    model = Plant
    template_name = 'app/plant_list.html'
    context_object_name = 'plants'

    def get_queryset(self):
        user_plants = Plant.objects.filter(user=self.request.user)
        public_plants = Plant.objects.filter(visibility='public')
        return user_plants | public_plants  # Union of user's plants and public plants


class PlantCreateView(CreateView):
    model = Plant
    template_name = 'app/add_plant.html'
    success_url = reverse_lazy('plant_list')
    fields = ['name', 'type', 'care_instructions', 'image', 'visibility']  # Include visibility field

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate the plant with the logged-in user
        return super().form_valid(form)


class PlantDetailView(DetailView):
    model = Plant
    template_name = 'app/plant_detail.html'
    context_object_name = 'plant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plant = self.get_object()
        context['health_updates'] = plant.health_updates.all()  # Get all health updates for the plant
        context['care_logs'] = plant.care_logs.all()  # Get all care logs for the plant
        context['reminders'] = plant.reminders.all()  # Get all reminders for the plant
        context['watering_schedules'] = plant.watering_schedules.all()  # Get all watering schedules for the plant
        return context

class PlantUpdateView(UpdateView):
    model = Plant
    form_class = PlantForm
    template_name = 'app/update_plant.html'
    context_object_name = 'plant'

    def get_object(self, queryset=None):
        # Use pk to fetch the plant object
        return get_object_or_404(Plant, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        # Redirect to the plant detail page after updating
        return reverse_lazy('plant_detail', kwargs={'pk': self.object.pk})

class HealthStatusCreateView(CreateView):
    model = HealthStatus
    form_class = HealthStatusForm
    template_name = 'app/add_health_status.html'

    def form_valid(self, form):
        plant = get_object_or_404(Plant, id=self.kwargs['plant_id'], user=self.request.user)
        form.instance.plant = plant  # Associate the health status with the plant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('plant_detail', kwargs={'pk': self.kwargs['plant_id']})


class CareLogCreateView(CreateView):
    model = CareLog
    form_class = CareLogForm
    template_name = 'app/add_care_log.html'

    def form_valid(self, form):
        plant = get_object_or_404(Plant, id=self.kwargs['plant_id'], user=self.request.user)
        form.instance.plant = plant  # Associate the care log with the plant
        return super().form_valid(form)

    def get_success_url(self):
        # Correctly reverse using 'pk' instead of 'plant_id'
        return reverse_lazy('plant_detail', kwargs={'pk': self.kwargs['plant_id']})


class ReminderCreateView(CreateView):
    model = Reminder
    form_class = ReminderForm
    template_name = 'app/add_reminder.html'

    def form_valid(self, form):
        plant = get_object_or_404(Plant, id=self.kwargs['plant_id'], user=self.request.user)
        form.instance.plant = plant  # Associate the reminder with the plant
        return super().form_valid(form)

    def get_success_url(self):
        # Correctly reverse using 'pk' instead of 'plant_id'
        return reverse_lazy('plant_detail', kwargs={'pk': self.kwargs['plant_id']})


class CompleteReminderView(View):
    def post(self, request, *args, **kwargs):
        reminder = get_object_or_404(Reminder, id=kwargs['reminder_id'])
        reminder.is_completed = True
        reminder.save()

        # After completing the reminder, redirect to the plant detail page
        return redirect(reverse_lazy('plant_detail', kwargs={'pk': reminder.plant.id}))



class PlantDeleteView(DeleteView):
    model = Plant
    template_name = 'app/delete_plant.html'
    context_object_name = 'plant'
    success_url = reverse_lazy('plant_list')  # Redirect to plant list after deletion

    def get_object(self):
        return get_object_or_404(Plant, id=self.kwargs['plant_id'], user=self.request.user)

class PlantSearchView(ListView):
    model = Plant
    template_name = 'app/plant_list.html'
    context_object_name = 'plants'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Plant.objects.filter(
            Q(user=self.request.user) & (Q(name__icontains=query) | Q(type__icontains=query))
        )


# Health Status Detail View
class HealthStatusDetailView(DetailView):
    model = HealthStatus
    template_name = 'app/health_status_detail.html'
    context_object_name = 'health_status'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        health_status = self.get_object()
        context['plant_id'] = health_status.plant.id  # Add the plant_id to the context if needed
        return context


class HealthStatusUpdateView(UpdateView):
    model = HealthStatus
    form_class = HealthStatusForm
    template_name = 'app/edit_health_status.html'

    def get_object(self):
        # Ensure the health status belongs to the logged-in user
        return get_object_or_404(HealthStatus, id=self.kwargs['status_id'], plant__user=self.request.user)

    def get_success_url(self):
        # Redirect to the plant detail view after a successful update
        return reverse_lazy('plant_detail', kwargs={'pk': self.object.plant.id})

class HealthStatusDeleteView(DeleteView):
    model = HealthStatus
    template_name = 'app/health_status_delete.html'

    def get_object(self, queryset=None):
        plant_id = self.kwargs.get('plant_id')
        status_id = self.kwargs.get('status_id')
        return get_object_or_404(HealthStatus, plant_id=plant_id, id=status_id)

    def get_success_url(self):
        return reverse_lazy('plant_detail', kwargs={'pk': self.object.plant_id})


# Care Log Detail View
class CareLogDetailView(DetailView):
    model = CareLog
    template_name = 'app/care_log_detail.html'
    context_object_name = 'care_log'


class CareLogUpdateView(UpdateView):
    model = CareLog
    form_class = CareLogForm
    template_name = 'app/edit_care_log.html'

    def get_object(self):
        care_log = get_object_or_404(CareLog, id=self.kwargs['log_id'], plant__user=self.request.user)
        return care_log

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['care_log'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('plant_detail', kwargs={'pk': self.object.plant.id})

class CareLogDeleteView(DeleteView):
    model = CareLog
    template_name = 'app/care_log_delete.html'

    def get_object(self):
        care_log = get_object_or_404(CareLog, id=self.kwargs['log_id'], plant__user=self.request.user)
        return care_log

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure care_log and care_log.plant are not None
        context['care_log'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('plant_detail', kwargs={'pk': self.object.plant.id})



# Reminder Detail View
class ReminderDetailView(DetailView):
    model = Reminder
    template_name = 'app/reminder_detail.html'
    context_object_name = 'reminder'


class ReminderUpdateView(UpdateView):
    model = Reminder
    form_class = ReminderForm
    template_name = 'app/edit_reminder.html'

    def get_object(self):
        # Ensure the reminder belongs to the logged-in user
        return get_object_or_404(Reminder, id=self.kwargs['reminder_id'], plant__user=self.request.user)

    def get_success_url(self):
        # Redirect to the plant detail view after a successful update
        return reverse_lazy('plant_detail', kwargs={'pk': self.object.plant.id})

class ReminderDeleteView(DeleteView):
    model = Reminder
    template_name = 'app/reminder_delete.html'

    def get_object(self, queryset=None):
        # Ensure that the Reminder belongs to the logged-in user
        return get_object_or_404(Reminder, id=self.kwargs['reminder_id'], plant__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('plant_detail', kwargs={'pk': self.object.plant.id})  # Correctly using plant.id


class WateringScheduleCreateView(CreateView):
    model = WateringSchedule
    form_class = WateringScheduleForm
    template_name = 'app/add_watering_schedule.html'

    def form_valid(self, form):
        plant = get_object_or_404(Plant, id=self.kwargs['plant_id'], user=self.request.user)
        form.instance.plant = plant  # Associate the watering schedule with the plant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('plant_detail', kwargs={'pk': self.kwargs['plant_id']})

class WateringScheduleDetailView(DetailView):
    model = WateringSchedule
    template_name = 'app/watering_schedule_detail.html'
    context_object_name = 'schedule'

    def get_object(self, queryset=None):
        return get_object_or_404(WateringSchedule, id=self.kwargs.get('pk'))

class WateringScheduleUpdateView(UpdateView):
    model = WateringSchedule
    form_class = WateringScheduleForm
    template_name = 'app/edit_watering_schedule.html'

    def get_object(self):
        watering_schedule = get_object_or_404(WateringSchedule, id=self.kwargs['schedule_id'])
        return watering_schedule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['watering_schedule'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('plant_detail', kwargs={'pk': self.object.plant.id})





class WateringScheduleDeleteView(DeleteView):
    model = WateringSchedule
    template_name = 'app/watering_schedule_delete.html'
    context_object_name = 'watering_schedule'

    def get_object(self, queryset=None):
        plant_id = self.kwargs.get('plant_id')
        schedule_id = self.kwargs.get('schedule_id')
        return get_object_or_404(WateringSchedule, plant_id=plant_id, id=schedule_id)

    def get_success_url(self):
        return reverse('plant_detail', kwargs={'pk': self.object.plant.id})