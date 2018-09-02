from django.db import models

# Create your models here.
class Data(models.Model):
    processes = models.CharField(null=False,max_length=25)
    courts = (
        ('MT', 'TJMS'),
        ('SP', 'TJSP'),
    )

    courts = models.CharField(max_length=5, choices=courts, default='RED')

    def publish(self):
        self.save()

    def __str__(self):
        return self.processes