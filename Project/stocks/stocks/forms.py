from django import forms
from datetime import datetime, timedelta

class FilterForm(forms.Form):

    today = datetime.now().date().strftime("%Y-%m-%d")
    yearAgo = (datetime.now().date() - timedelta(days=365)).strftime("%Y-%m-%d")

    start = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date', 'max': today, 'value': yearAgo}))
    end = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date', 'max': today, 'value': today}))

class AddForm(forms.Form):

    today = datetime.now().date().strftime("%Y-%m-%d")
    yearAgo = (datetime.now().date() - timedelta(days=365)).strftime("%Y-%m-%d")


    ticker = forms.CharField(label='Ticker', max_length=10)
    action = forms.ChoiceField(label='Action', choices=[('add', 'Add'), ('remove', 'Remove')])

    start = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date', 'max': today, 'min': '2016-01-01', 'value': '2016-01-01'})) # Due to limitations with Alpaca, we cannot get data before 2016

class PredictForm(forms.Form):

    tomorrow = (datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d")

    predictUntil = forms.DateField(label='Prediction End', widget=forms.DateInput(attrs={'type': 'date', 'min': '2016-01-01', 'value': tomorrow}))