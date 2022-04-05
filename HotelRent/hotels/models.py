from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=128)


class City(models.Model):
    city = models.CharField(max_length=128)


class Hotel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='hotel_images', default='hotel_images/empty.png')
    adress = models.CharField(max_length=128)
    price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sort_date = models.DateTimeField(auto_now=True)

