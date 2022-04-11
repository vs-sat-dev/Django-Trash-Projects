from django.contrib import admin

from .models import Hotel, Category, Facilities, State, Region, City


admin.site.register(Hotel)
admin.site.register(Category)
admin.site.register(Facilities)
admin.site.register(State)
admin.site.register(Region)
admin.site.register(City)

