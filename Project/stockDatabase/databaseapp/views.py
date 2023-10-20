from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock
# Create your views here.

def stockPageView(request):
    data = Stock.objects.all()
    context = {"stocks": data}
    return render(request, 'databaseapp/stock.html', context)
