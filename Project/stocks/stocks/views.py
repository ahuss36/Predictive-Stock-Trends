from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Stock
from . import alpaca
import pandas
from datetime import datetime, timedelta
import time
import threading
import os

from .forms import *

from . import lstm


def home(request):

    raw = Stock.objects.all()
    rawTickers = []

    form = AddForm()

    for i in raw:
        rawTickers.append(i.ticker)

    tickers = set(rawTickers)

    return render(request, 'stocks/home.html', {'tickers': tickers, 'form': form})

def renderHome(request, message = None):
    
        raw = Stock.objects.all()
        rawTickers = []
    
        form = AddForm()
    
        for i in raw:
            rawTickers.append(i.ticker)
    
        tickers = set(rawTickers)
    
        return render(request, 'stocks/home.html', {'tickers': tickers, 'form': form, 'message': message})

def add_data(ticker, action, start): 
    # add data to a the database given a ticker
    # this is meant to be fired into a different thread instead of run in sequence

    today = datetime.now().date().strftime("%Y-%m-%d")

    # pull raw data from alpaca
    session = alpaca.session()
    data = session.get_history(ticker, "1D", start)

    # pull existing data from database
    tickerPastData = Stock.objects.filter(ticker=ticker)

    # get list of dates that we already have data for
    dates = []
    for i in tickerPastData:
        print(i.date)
        dates.append(i.date)

    # add everything to database
    for index, row in data.iterrows():
        # get the entry's date
        time_obj = pandas.to_datetime(row["time"], unit="s")
        timestamp = time_obj.to_pydatetime().date()

        # prevent duplication
        if(timestamp not in dates):
            stock = Stock(ticker=ticker, close=row["close"], date=timestamp)
            stock.save()

def add(request): # this also serves as the remove function, I am just bad at naming things

    ticker = request.POST.get('ticker')

    action = request.POST.get('action')

    if ticker is None:
        return render(request, 'stocks/home.html')

    if action == "add":

        # get start date from request, and convert it into a datetime date object
        start_raw = request.POST.get('start')
        start = datetime.strptime(start_raw, "%Y-%m-%d").date()

        # fire off add_data function into a separate thread since it is slow
        task = threading.Thread(target=add_data, args=(ticker, action, start))
        task.start()

        message = "Data is being pulled, please wait for it to finish."
    
    elif action == "remove":
            
        Stock.objects.filter(ticker=ticker).delete()
        message = "Data has been removed."


    return renderHome(request, message)

def getPriceData(ticker, timespan = None):
    realData = Stock.objects.filter(ticker=ticker, prediction=False)
    predictData = Stock.objects.filter(ticker=ticker, prediction=True)

    if (timespan != None):
        startTime = datetime.fromtimestamp(int(timespan.split("-")[0]))
        endTime = datetime.fromtimestamp(int(timespan.split("-")[1]))

        realData = Stock.objects.filter(ticker=ticker, prediction=False, date__range=[startTime, endTime])
        predictData = Stock.objects.filter(ticker=ticker, prediction=True, date__range=[startTime, endTime])
    else:
        realData = Stock.objects.filter(ticker=ticker, prediction=False)
        predictData = Stock.objects.filter(ticker=ticker, prediction=True)

    return realData, predictData

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

    realData, predictData = getPriceData(ticker, timespan)
    name = realData[0].ticker

    filterForm = FilterForm()
    predictForm = PredictForm()
    deleteForm = DeleteModelForm()

    forms = {
        'filterForm': filterForm,
        'predictForm': predictForm,
        'deleteForm': deleteForm
    }

    args = {
        'modelExists': os.path.isfile(f"stocks/models/{ticker}.keras"),
        'hasPredictions': Stock.objects.filter(ticker=ticker, prediction=True).count() > 0,
    }

    return render(request, 'stocks/detail.html', {'realData': realData, 'predictData': predictData, 'name': name, 'forms': forms, 'args': args})

def predict(request, ticker):
    form = PredictForm(request.POST)

    if form.is_valid():
        daysOut = form.cleaned_data['predictUntil']
    else:
        return False
    
    # convert daysOut (a date string) to the number of days between now and then
    daysOut = datetime.strptime(str(daysOut), "%Y-%m-%d").date() - datetime.now().date()

    daysOut = daysOut.days # daysOut was previously some sort of duration object, this converts it to an int

    # throw the predict_data function into a separate thread since it is slow
    task = threading.Thread(target=predict_thread, args=(ticker, daysOut))
    task.start()

    return detail(request, ticker)

def predict_thread(ticker, daysOut):

    print(f"Starting prediction for {daysOut} days out for {ticker}")
        
    lstm.predict(ticker, daysOut)

    return True

def deleteModel(request, ticker):
    # delete model file

    print(f"Deleting model for {ticker}")

    if (request.method == "GET"): # catch if this is a GET request, just send the user to their corresponding detail page
        return HttpResponseRedirect('/detail/' + ticker)
    
    if (request.method == "POST"):
        form = DeleteModelForm(request.POST)

        if form.is_valid():
            confirm = form.cleaned_data['confirm']
        else:
            return False
        
        if (confirm):
            os.remove(f"stocks/models/{ticker}.keras")
            print(f"Model for {ticker} deleted")
            return HttpResponseRedirect('/detail/' + ticker)
        
def deletePredictions(request, ticker):
    
    # delete predictions from database

    predictions = Stock.objects.filter(ticker=ticker, prediction=True)

    for i in predictions:
        i.delete()

    return HttpResponseRedirect('/detail/' + ticker)