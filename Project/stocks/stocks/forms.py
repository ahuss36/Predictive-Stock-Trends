from django import forms
from datetime import datetime, timedelta
import os

class FilterForm(forms.Form):

    today = datetime.now().date().strftime("%Y-%m-%d")
    sevenDaysOut = ((datetime.now().date() + timedelta(days=1)) + timedelta(days=6)).strftime("%Y-%m-%d")
    yearAgo = (datetime.now().date() - timedelta(days=365)).strftime("%Y-%m-%d")

    start = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date', 'max': sevenDaysOut, 'value': yearAgo}))
    end = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date', 'max': sevenDaysOut, 'value': today}))

class AddForm(forms.Form): # form to add ticker data

    today = datetime.now().date().strftime("%Y-%m-%d")
    yearAgo = (datetime.now().date() - timedelta(days=365)).strftime("%Y-%m-%d")


    ticker = forms.CharField(label='Ticker', max_length=10)
    action = forms.ChoiceField(label='Action', choices=[('add', 'Add'), ('remove', 'Remove')])

    start = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date', 'max': today, 'min': '2016-01-01', 'value': '2016-01-01'})) # Due to limitations with Alpaca, we cannot get data before 2016

class PredictForm(forms.Form): # form to request stock predictions

    tomorrow = (datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d")
    sevenDaysOut = ((datetime.now().date() + timedelta(days=1)) + timedelta(days=6)).strftime("%Y-%m-%d")

    predictUntil = forms.DateField(label='Prediction End', widget=forms.DateInput(attrs={'type': 'date', 'min': tomorrow, 'max': sevenDaysOut, 'value': tomorrow}))

class DeleteModelForm(forms.Form): # form to delete a model
    # confirm checkbox
    confirm = forms.BooleanField(label='Confirm', required=True)

class DeletePredictionsForm(forms.Form): # form to delete predictions
    # confirm checkbox
    confirm = forms.BooleanField(label='Confirm', required=True)