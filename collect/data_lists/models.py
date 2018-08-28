from django.db import models

# Create your models here.
class Data(models.Model):
    Processos = models.CharField(max_length=200)
    courts = (
        ('MT', 'TJSP'),
        ('SP', 'TJMS'),
    )

    Tribunais = models.CharField(max_length=5, choices=courts, default='RED')

    def publish(self):
        self.save()

    def __str__(self):
        return self.Processos