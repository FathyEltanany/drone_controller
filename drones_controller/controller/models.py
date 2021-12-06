from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
drone_model_choices = (
    ('Lightweight', 'Lightweight'),
    ('Middleweight', 'Middleweight'),
    ('Cruiserweight', 'Cruiserweight'),
    ('Heavyweight', 'Heavyweight')
)

drone_state_choices = (
    ('IDLE', 'IDLE'),
    ('LOADING', 'LOADING'),
    ('LOADED', 'LOADED'),
    ('DELIVERING', 'DELIVERING'),
    ('DELIVERED', 'DELIVERED'),
    ('RETURNING', 'RETURNING')
)


class Drone(models.Model):
    serial_number = models.CharField(max_length=100,unique=True)
    model = models.CharField(choices=drone_model_choices, max_length=20)
    weight_limit = models.IntegerField(validators=[MaxValueValidator(100)])
    battery_capacity = models.IntegerField(validators=[MaxValueValidator(100)])
    state = models.CharField(choices=drone_state_choices, max_length=20)
    # medications = models.OneTo

    def __str__(self):
        return self.serial_number


class Medication(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    weight = models.IntegerField()
    image = models.ImageField()
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, blank=True,null=True)
