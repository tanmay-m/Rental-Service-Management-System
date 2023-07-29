from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=255,null=True, blank=True)
    brand = models.CharField(max_length=255,null=True, blank=True)
    category = models.CharField(max_length=255,null=True, blank=True)
    owner = models.CharField(max_length=255,null=True, blank=True)
    rating = models.FloatField(max_length=255,null=True, blank=True)
    distance = models.FloatField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.name