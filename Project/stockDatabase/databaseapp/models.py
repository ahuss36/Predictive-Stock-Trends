from django.db import models

# Create your models here.

class Stock(models.Model):
    stock_name = models.CharField(max_length=4, unique = True)
    stock_predicted = models.IntegerField(default=0)

    def __str__(self):
        return (self.stock_name + " $" + str(self.stock_predicted))

