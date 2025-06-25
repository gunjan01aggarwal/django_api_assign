from django.db import models

# Create your models here.
class Employees(models.Model):
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
    emp_id=models.IntegerField()
    salary=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.first_name

class Telegram(models.Model):
    username=models.CharField(max_length=10)        