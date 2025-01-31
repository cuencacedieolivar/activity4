from django.db import models
from django.urls import reverse
from django.conf import settings



class Plant(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    care_instructions = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
        return self.plant

    def get_absolute_url(self):
        return reverse('health_status_detail', kwargs={'pk': self.pk})




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
        return self.water_frequency

    def get_absolute_url(self):
        return reverse('watering_schedule_detail', kwargs={'pk': self.pk})

class Reminder(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    reminder_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task

    def get_absolute_url(self):
        return reverse('reminder_detail', kwargs={'pk': self.pk})