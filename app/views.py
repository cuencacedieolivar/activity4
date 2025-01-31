from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Plant, HealthStatus, CareLog, WateringSchedule, Reminder


class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class ContactPageView(TemplateView):
    template_name = 'app/contact.html'


# Plant Views
class PlantListView(ListView):
    model = Plant
    template_name = 'plants/plant_list.html'
    context_object_name = 'plants'

class PlantDetailView(DetailView):
    model = Plant
    template_name = 'plants/plant_detail.html'

class PlantCreateView(CreateView):
    model = Plant
    fields = ['name', 'type', 'care_instructions', 'image']
    template_name = 'plants/plant_create.html'

    def form_valid(self, form):
        # Automatically associate the plant with the logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlantUpdateView(UpdateView):
    model = Plant
    fields = ['name', 'type', 'care_instructions', 'image']
    template_name = 'plants/plant_update.html'

class PlantDeleteView(DeleteView):
    model = Plant
    template_name = 'plants/plant_delete.html'
    success_url = reverse_lazy('plant_list')

# HealthStatus Views
class HealthStatusListView(ListView):
    model = HealthStatus
    template_name = 'health/health_status_list.html'
    context_object_name = 'statuses'

class HealthStatusDetailView(DetailView):
    model = HealthStatus
    template_name = 'health/health_status_detail.html'
    context_object_name = 'status'

class HealthStatusCreateView(CreateView):
    model = HealthStatus
    fields = ['plant', 'status', 'notes']
    template_name = 'health/health_status_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter plants owned by the logged-in user
        context['plants'] = Plant.objects.filter(user=self.request.user)

        # Check if the plant_id is passed as a query parameter
        plant_id = self.request.GET.get('plant_id')
        if plant_id:
            plant = Plant.objects.filter(id=plant_id, user=self.request.user).first()
            if plant:
                context['selected_plant'] = plant
        return context

    def form_valid(self, form):
        # Automatically associate the selected plant
        plant_id = self.request.GET.get('plant_id')
        if plant_id:
            plant = Plant.objects.filter(id=plant_id, user=self.request.user).first()
            if plant:
                form.instance.plant = plant
        return super().form_valid(form)

class HealthStatusUpdateView(UpdateView):
    model = HealthStatus
    fields = ['status', 'notes']
    template_name = 'health/health_status_update.html'

class HealthStatusDeleteView(DeleteView):
    model = HealthStatus
    template_name = 'health/health_status_delete.html'
    success_url = reverse_lazy('health_status_list')

# CareLog Views
class CareLogListView(ListView):
    model = CareLog
    template_name = 'log/care_log_list.html'
    context_object_name = 'cares'

class CareLogDetailView(DetailView):
    model = CareLog
    template_name = 'log/care_log_detail.html'
    context_object_name = 'care'

class CareLogCreateView(CreateView):
    model = CareLog
    fields = ['plant', 'action', 'notes']
    template_name = 'log/care_log_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter plants owned by the logged-in user
        context['plants'] = Plant.objects.filter(user=self.request.user)
        # Check if 'plant_id' is in the query parameters
        plant_id = self.request.GET.get('plant_id')
        if plant_id:
            context['selected_plant'] = Plant.objects.get(id=plant_id)  # This will pre-select the plant
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate care log with logged-in user
        return super().form_valid(form)


class CareLogUpdateView(UpdateView):
    model = CareLog
    fields = ['action', 'notes']
    template_name = 'log/care_log_update.html'

class CareLogDeleteView(DeleteView):
    model = CareLog
    template_name = 'log/care_log_delete.html'
    success_url = reverse_lazy('care_log_list')

# WateringSchedule Views
class WateringScheduleListView(ListView):
    model = WateringSchedule
    template_name = 'schedule/watering_schedule_list.html'
    context_object_name = 'schedules'

class WateringScheduleDetailView(DetailView):
    model = WateringSchedule
    template_name = 'schedule/watering_schedule_detail.html'
    context_object_name = 'schedule'


class WateringScheduleCreateView(CreateView):
    model = WateringSchedule
    fields = ['plant', 'water_frequency', 'last_watered', 'next_watering']
    template_name = 'schedule/watering_schedule_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plants'] = Plant.objects.filter(user=self.request.user)
        plant_id = self.request.GET.get('plant_id')
        if plant_id:
            context['selected_plant'] = Plant.objects.get(id=plant_id)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WateringScheduleUpdateView(UpdateView):
    model = WateringSchedule
    fields = ['water_frequency', 'last_watered', 'next_watering']
    template_name = 'schedule/watering_schedule_update.html'

class WateringScheduleDeleteView(DeleteView):
    model = WateringSchedule
    template_name = 'schedule/watering_schedule_delete.html'
    success_url = reverse_lazy('watering_schedule_list')

# Reminder Views
class ReminderListView(ListView):
    model = Reminder
    template_name = 'reminder/reminder_list.html'
    context_object_name = 'reminders'

class ReminderDetailView(DetailView):
    model = Reminder
    template_name = 'reminder/reminder_detail.html'
    context_object_name = 'reminder'

class ReminderCreateView(CreateView):
    model = Reminder
    fields = ['plant', 'task', 'reminder_time', 'is_completed']
    template_name = 'reminder/reminder_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plants'] = Plant.objects.filter(user=self.request.user)
        plant_id = self.request.GET.get('plant_id')
        if plant_id:
            context['selected_plant'] = Plant.objects.get(id=plant_id)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user  # Associate reminder with logged-in user
        return super().form_valid(form)

class ReminderUpdateView(UpdateView):
    model = Reminder
    fields = ['task', 'reminder_time', 'is_completed']
    template_name = 'reminder/reminder_update.html'

class ReminderDeleteView(DeleteView):
    model = Reminder
    template_name = 'reminder/reminder_delete.html'
    success_url = reverse_lazy('reminder_list')
