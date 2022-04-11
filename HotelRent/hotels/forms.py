from django import forms
from ckeditor.fields import RichTextField

from .models import Hotel


class HotelSearchForm(forms.Form):
    category = forms.CharField(required=False)
    city = forms.CharField(required=False)
    text = forms.CharField(required=False)


class CreateHotelForm(forms.ModelForm):
    title = forms.CharField(max_length=64)
    image = forms.ImageField(required=False, widget=forms.FileInput(), max_length=128)
    price = forms.IntegerField()

    description = RichTextField()

    """category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    facilities = models.ForeignKey(Facilities, on_delete=models.CASCADE)"""

    street = forms.CharField(max_length=64)
    house = forms.CharField(max_length=64)
    adress = forms.CharField(max_length=256)
    coord_x = forms.FloatField()
    coord_y = forms.FloatField()

    class Meta:
        model = Hotel
        fields = '__all__'
        exclude = ['created', 'updated', 'sort_date']
