from django.db import models
from django.contrib.auth.models import User
from django_unique_slugify import unique_slugify
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
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True, db_index=True)
    image = models.ImageField(upload_to='hotel_images', default='hotel_images/empty.png')
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sort_date = models.DateTimeField(auto_now_add=True)

    description = RichTextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title, slug_field_name='slug')
        super().save(*args, **kwargs)

