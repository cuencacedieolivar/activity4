from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (CustomLoginView, RegisterView,
                    CustomLogoutView,
                    HomePageView,
                    PlantListView,
                    PlantDetailView,
                    PlantCreateView,
                    HealthStatusCreateView,
                    CareLogCreateView,
                    ReminderCreateView,
                    CompleteReminderView,
                    PlantDeleteView,
                    PlantSearchView,
                    HealthStatusDetailView,
                    HealthStatusUpdateView,
                    HealthStatusDeleteView,
                    CareLogDetailView,
                    CareLogUpdateView,
                    CareLogDeleteView,
                    ReminderDetailView,
                    ReminderUpdateView,
                    ReminderDeleteView,
                    WateringScheduleDetailView,
                    WateringScheduleCreateView,
                    WateringScheduleUpdateView,
                    WateringScheduleDeleteView,
                    PlantUpdateView
                    )

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('home/', HomePageView.as_view(), name='home'),

    path('plants/', PlantListView.as_view(), name='plant_list'),  # List all plants
    path('plant/<int:pk>/', PlantDetailView.as_view(), name='plant_detail'),  # View plant details
    path('plant/add/', PlantCreateView.as_view(), name='add_plant'),  # Add new plant
    path('plant/<int:plant_id>/health-status/add/',HealthStatusCreateView.as_view(), name='add_health_status'),  # Add health status
    path('plant/<int:plant_id>/care-log/add/', CareLogCreateView.as_view(), name='add_care_log'),  # Add care log
    path('plant/<int:plant_id>/reminder/add/', ReminderCreateView.as_view(), name='add_reminder'),  # Add reminder
    path('plant/reminder/<int:reminder_id>/complete/', CompleteReminderView.as_view(), name='complete_reminder'),  # Mark reminder as complete
    path('plant/<int:plant_id>/delete/', PlantDeleteView.as_view(), name='delete_plant'),  # Delete plant
    path('plant/search/', PlantSearchView.as_view(), name='search_plants'),  # Search plants

    # Plant details page
    path('plant/<int:pk>/', PlantDetailView.as_view(), name='plant_detail'),
    path('plant/update/<int:pk>/', PlantUpdateView.as_view(), name='update_plant'),

    # Health status detail page
    path('health-status/<int:pk>/', HealthStatusDetailView.as_view(), name='health_status_detail'),
    path('plant/<int:plant_id>/health_status/<int:status_id>/edit/', HealthStatusUpdateView.as_view(),
         name='edit_health_status'),
    path('plant/<int:plant_id>/health_status/<int:status_id>/delete/', HealthStatusDeleteView.as_view(),
         name='health_status_delete'),
    # Care log detail page
    path('care-log/<int:pk>/', CareLogDetailView.as_view(), name='care_log_detail'),
    path('plant/<int:plant_id>/care_log/<int:log_id>/edit/', CareLogUpdateView.as_view(), name='edit_care_log'),
    path('plant/<int:plant_id>/care_log/<int:log_id>/delete/', CareLogDeleteView.as_view(),
         name='delete_care_log'),

    # Reminder detail page
    path('reminder/<int:pk>/', ReminderDetailView.as_view(), name='reminder_detail'),
    path('plant/<int:plant_id>/reminder/<int:reminder_id>/edit/', ReminderUpdateView.as_view(),
         name='edit_reminder'),
    path('plant/<int:plant_id>/reminder/<int:reminder_id>/delete/', ReminderDeleteView.as_view(),
         name='delete_reminder'),

    path('watering_schedule/<int:pk>/', WateringScheduleDetailView.as_view(), name='watering_schedule_detail'),
    path('plant/<int:plant_id>/add_watering_schedule/',WateringScheduleCreateView.as_view(), name='add_watering_schedule'),
    path('watering_schedule/<int:schedule_id>/edit/', WateringScheduleUpdateView.as_view(), name='edit_watering_schedule'),
    path('watering_schedule/delete/<int:plant_id>/<int:schedule_id>/', WateringScheduleDeleteView.as_view(), name='watering_schedule_delete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
