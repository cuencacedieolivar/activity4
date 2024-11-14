from django.db import models
from django.contrib.auth.models import User




class Plant(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    care_instructions = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='plant_images/', blank=True, null=True)
    visibility = models.CharField(
        max_length=7,
        choices=VISIBILITY_CHOICES,
        default='public',  # Default visibility is public
    )

    def __str__(self):
        return self.name


class HealthStatus(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='health_updates')
    status = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.plant.name} - {self.status} - {self.update_time}"

class CustomUser(User):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username


class CareLog(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='care_logs')
    action = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.plant.name} - {self.action} - {self.date}"

class WateringSchedule(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='watering_schedules')
    water_frequency = models.CharField(
        max_length=50,
        choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Bi-weekly', 'Bi-weekly')],
        default='Weekly'
    )
    last_watered = models.DateField(blank=True, null=True)
    next_watering = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Watering schedule for {self.plant.name} - Next watering: {self.next_watering}"

class Reminder(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='reminders')
    task = models.CharField(max_length=100)
    reminder_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.plant.name} - {self.task} - {self.reminder_time}"