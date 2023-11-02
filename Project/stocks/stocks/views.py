from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Stock
from . import alpaca
import pandas
from datetime import datetime
import time

from .forms import FilterForm


def home(request):

    raw = Stock.objects.all()
    rawTickers = []

    for i in raw:
        rawTickers.append(i.ticker)

    tickers = set(rawTickers)

    return render(request, 'stocks/home.html', {'tickers': tickers})

def add(request):
    ticker = request.POST.get('ticker')


    action = request.POST.get('action')

    if ticker is not None and action == "add":

        session = alpaca.session()
        data = session.get_history(ticker, "1D", "2020-01-01")

        for index, row in data.iterrows():
            time_obj = pandas.to_datetime(row["time"], unit="s")
            timestamp = time_obj.to_pydatetime().date()

            stock = Stock(ticker=ticker, close=row["close"], date=timestamp)
            stock.save()

        return HttpResponseRedirect('/')
    
    elif ticker is not None and action == "remove":
            
            print("Removing " + ticker)
            
            Stock.objects.filter(ticker=ticker).delete()
    
            return HttpResponseRedirect('/')

    return render(request, 'stocks/add.html')

def detail(request, ticker):

    timespan = None

    if (request.method == "POST"):
        form = FilterForm(request.POST)

        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']

            timespan = str(int(time.mktime(start.timetuple()))) + "-" + str(int(time.mktime(end.timetuple())))

    data = Stock.objects.filter(ticker=ticker)
    name = data[0].ticker

    form = FilterForm()

    if (timespan == None):
        return render(request, 'stocks/detail.html', {'data': data, 'name': name, 'form': form})
    
    # if we get to here, timespan is defined. It is [unixtime_start]-[unixtime_end] to allow it to be fed via a URL

    startTime = datetime.fromtimestamp(int(timespan.split("-")[0]))
    endTime = datetime.fromtimestamp(int(timespan.split("-")[1]))
    
    data = Stock.objects.filter(ticker=ticker, date__range=[startTime, endTime])

    return render(request, 'stocks/detail.html', {'data': data, 'name': name, 'form': form})