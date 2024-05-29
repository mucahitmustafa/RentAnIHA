from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    added_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Iha(models.Model):
    brand = models.CharField(max_length=25)
    model = models.CharField(max_length=70)
    weight = models.IntegerField()
    serial_number = models.CharField(max_length=20, unique=True)
    added_date = models.DateTimeField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.brand} - {self.model}"


class Rental(models.Model):
    iha = models.ForeignKey("Iha", on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    start_date = models.DateField()
    end_date = models.DateField()
    is_returned = models.BooleanField(default=False)
