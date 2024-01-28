from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=25, null=False, blank=False, unique=True)
    password = models.CharField(max_length=100)
    repetitions = models.IntegerField(default=10)  # Number of repeat for hashing

    def __str__(self):
        return f'{self.username}-{self.repetitions}'
