from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Stock
from . import alpaca
import pandas
from datetime import datetime, timedelta
import time
import threading

from .forms import FilterForm, AddForm


def home(request):

    raw = Stock.objects.all()
    rawTickers = []

    form = AddForm()

    for i in raw:
        rawTickers.append(i.ticker)

    tickers = set(rawTickers)

    return render(request, 'stocks/home.html', {'tickers': tickers, 'form': form})

def add_data(ticker, action, start):

    today = datetime.now().date().strftime("%Y-%m-%d")

    session = alpaca.session()
    data = session.get_history(ticker, "1D", start)

    for index, row in data.iterrows():
        time_obj = pandas.to_datetime(row["time"], unit="s")
        timestamp = time_obj.to_pydatetime().date()

        stock = Stock(ticker=ticker, close=row["close"], date=timestamp)
        stock.save()
    

def add(request):

    ticker = request.POST.get('ticker')

    action = request.POST.get('action')

    if ticker is not None and action == "add":

        ticker = request.POST.get('ticker')
        action = request.POST.get('action')
        start_raw = request.POST.get('start')

        start = datetime.strptime(start_raw, "%Y-%m-%d").date()

        task = threading.Thread(target=add_data, args=(ticker, action, start))

        task.start()

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

            try:
                # timespan is a string that looks like this: [unixtime_start]-[unixtime_end]
                timespan = str(int(time.mktime(start.timetuple()))) + "-" + str(int(time.mktime(end.timetuple())))
            except OverflowError:
                timespan = "0-" + str(int(time.mktime(end.timetuple())))

    # TODO: only get data from database once

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