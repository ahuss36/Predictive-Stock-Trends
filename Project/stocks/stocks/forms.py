from django import forms
from datetime import datetime

class FilterForm(forms.Form):

    today = datetime.now().date().strftime("%Y-%m-%d")

    start = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date', 'max': today}))
    end = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date', 'max': today}))