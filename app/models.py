from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse




class Plant(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    care_instructions = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='plant_images/', blank=True, null=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plant_detail', kwargs={'pk': self.pk})



class HealthStatus(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.plant.name

class CustomUser(User):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username


class CareLog(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.plant.name

    def get_absolute_url(self):
        return reverse('care_log_detail', kwargs={'pk': self.pk})


class WateringSchedule(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    water_frequency = models.CharField(
        max_length=50,
        choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Bi-weekly', 'Bi-weekly')],
        default='Weekly'
    )
    last_watered = models.DateField(blank=True, null=True)
    next_watering = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.plant.name

class Reminder(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    reminder_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return  self.plant.name