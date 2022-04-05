from django import forms


class HotelSearchForm(forms.Form):
    category = forms.CharField()
    city = forms.CharField()
    text = forms.CharField()
