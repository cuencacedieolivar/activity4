from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView, AboutPageView, ContactPageView,
    PlantListView, PlantDetailView, PlantCreateView, PlantUpdateView, PlantDeleteView,
    HealthStatusListView, HealthStatusDetailView, HealthStatusCreateView, HealthStatusUpdateView, HealthStatusDeleteView,
    CareLogListView, CareLogDetailView, CareLogCreateView, CareLogUpdateView, CareLogDeleteView,
    WateringScheduleListView, WateringScheduleDetailView, WateringScheduleCreateView, WateringScheduleUpdateView, WateringScheduleDeleteView,
    ReminderListView, ReminderDetailView, ReminderCreateView, ReminderUpdateView, ReminderDeleteView
)

urlpatterns = [
    # Static Pages
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),

    # Plant URLs
    path('plants/', PlantListView.as_view(), name='plant_list'),
    path('plants/<int:pk>/', PlantDetailView.as_view(), name='plant_detail'),
    path('plants/new/', PlantCreateView.as_view(), name='plant_create'),
    path('plants/<int:pk>/edit/', PlantUpdateView.as_view(), name='plant_update'),
    path('plants/<int:pk>/delete/', PlantDeleteView.as_view(), name='plant_delete'),

    # Health Status URLs
    path('health/', HealthStatusListView.as_view(), name='health_status_list'),
    path('health/<int:pk>/', HealthStatusDetailView.as_view(), name='health_status_detail'),
    path('health/new/', HealthStatusCreateView.as_view(), name='health_status_create'),
    path('health/<int:pk>/edit/', HealthStatusUpdateView.as_view(), name='health_status_update'),
    path('health/<int:pk>/delete/', HealthStatusDeleteView.as_view(), name='health_status_delete'),

    # Care Log URLs
    path('care-logs/', CareLogListView.as_view(), name='care_log_list'),
    path('care-logs/<int:pk>/', CareLogDetailView.as_view(), name='care_log_detail'),
    path('care-logs/new/', CareLogCreateView.as_view(), name='care_log_create'),
    path('care-logs/<int:pk>/edit/', CareLogUpdateView.as_view(), name='care_log_update'),
    path('care-logs/<int:pk>/delete/', CareLogDeleteView.as_view(), name='care_log_delete'),

    # Watering Schedule URLs
    path('watering-schedules/', WateringScheduleListView.as_view(), name='watering_schedule_list'),
    path('watering-schedules/<int:pk>/', WateringScheduleDetailView.as_view(), name='watering_schedule_detail'),
    path('watering-schedules/new/', WateringScheduleCreateView.as_view(), name='watering_schedule_create'),
    path('watering-schedules/<int:pk>/edit/', WateringScheduleUpdateView.as_view(), name='watering_schedule_update'),
    path('watering-schedules/<int:pk>/delete/', WateringScheduleDeleteView.as_view(), name='watering_schedule_delete'),

    # Reminder URLs
    path('reminders/', ReminderListView.as_view(), name='reminder_list'),
    path('reminders/<int:pk>/', ReminderDetailView.as_view(), name='reminder_detail'),
    path('reminders/new/', ReminderCreateView.as_view(), name='reminder_create'),
    path('reminders/<int:pk>/edit/', ReminderUpdateView.as_view(), name='reminder_update'),
    path('reminders/<int:pk>/delete/', ReminderDeleteView.as_view(), name='reminder_delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
