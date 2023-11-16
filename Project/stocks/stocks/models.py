from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    close = models.FloatField()
    date = models.DateField()
    prediction = models.BooleanField(default=False)
    
    def __str__(self):
        return self.ticker + ": $" + str(self.close) + " on " + str(self.date) + " REAL: " + str(not self.prediction)