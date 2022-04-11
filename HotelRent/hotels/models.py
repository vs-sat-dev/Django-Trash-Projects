from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category


class State(models.Model):
    state = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.state


class Region(models.Model):
    region = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.region


class City(models.Model):
    city = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.city


class Facilities(models.Model):
    facilities = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.facilities


class Hotel(models.Model):
    title = models.CharField(max_length=64)
    image = models.ImageField(upload_to='hotel_images', default='hotel_images/empty.png')
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sort_date = models.DateTimeField(auto_now=True)

    description = RichTextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    facilities = models.ForeignKey(Facilities, on_delete=models.CASCADE)

    street = models.CharField(max_length=64)
    house = models.CharField(max_length=64)
    adress = models.CharField(max_length=256)
    coord_x = models.FloatField()
    coord_y = models.FloatField()

