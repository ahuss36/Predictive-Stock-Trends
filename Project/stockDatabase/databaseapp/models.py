from django.db import models

# Create your models here.

class Stock(models.Model):
    stock_ticker = models.TextField(default='')
    stock_date = models.IntegerField(default=0)
    stock_close_price = models.FloatField(default=0.0)
    stock_prediction = models.BooleanField(default=False)

    def __str__(self):
        return (self.stock_ticker + " $" + str(self.stock_close_price))

