from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator

from .forms import HotelSearchForm, CreateHotelForm
from .models import Hotel, Category, Facilities, State, Region, City


def hotels(request):
    if request.method == 'POST':
        form = HotelSearchForm(request.POST)
        if form.is_valid():
            hotels_found = Hotel.objects.filter(
                Q(category__category__icontains=form.data['category']) &
                Q(city__city__icontains=form.data['city']) &
                (Q(description__icontains=form.data['text']) |
                 (Q(title__icontains=form.data['text'])))
            ).order_by('-updated')

            p = Paginator(hotels_found, 20)
            page = request.GET.get('page')
            hotels_paginated = p.get_page(page)

            context = {'form': form, 'hotels': hotels_paginated, 'category': form.data['category'],
                       'text': form.data['text'], 'city': form.data['city']}
            return render(request, 'hotels.html', context=context)
    else:

        """import random
        categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']
        facilities = ['Facilities 1', 'Facilities 2', 'Facilities 3']
        states = ['State 1', 'State 2', 'State 3']
        regions = ['Region 1', 'Region 2', 'Region 3']
        cities = ['City 1', 'City 2', 'City 3']
        for i in range(100):
            category = Category.objects.get(category=random.choice(categories))
            facility = Facilities.objects.get(facilities=random.choice(facilities))
            state = State.objects.get(state=random.choice(states))
            region = Region.objects.get(region=random.choice(regions))
            city = City.objects.get(city=random.choice(cities))
            Hotel.objects.create(title=f'Title {i}', description=f'Description of the hotel {i}', price=i*100,
                                 category=category, facilities=facility, state=state, region=region, city=city,
                                 street=f'Street {i}', house=f'House {i}', adress=f'Street {i} House {i}',
                                 coord_x=float(i), coord_y=float(100.0 - i))"""

        form = HotelSearchForm()
        category = request.GET.get('category')
        text = request.GET.get('text')
        city = request.GET.get('city')
        p = Paginator(Hotel.objects.filter(
            Q(category__category__icontains=category) &
            Q(city__city__icontains=city) &
            (Q(description__icontains=text) |
             (Q(title__icontains=text)))
        ).order_by('-updated'), 20)
        page = request.GET.get('page')
        hotels_paginated = p.get_page(page)
        context = {'form': form, 'hotels': hotels_paginated, 'category': category, 'text': text, 'city': city}
        return render(request, 'hotels.html', context=context)


def hotel_detail(request, city, category, title):
    hotel = Hotel.objects.filter(Q(city__city=city),
                                 Q(category__category=category),
                                 Q(title=title)).first()
    context = {'hotel': hotel}
    return render(request, 'hotel-detail.html', context=context)


def create_hotel(request):
    if request.method == 'POST':
        form = CreateHotelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = form.save()
            category = data.category
            city = data.city
            title = data.title
            return redirect(f'hotel-detail/{city}/{category}/{title}')
        else:
            context = {'form': form}
            return render(request, 'create-hotel.html', context=context)
    else:
        form = CreateHotelForm()
        context = {'form': form}
        return render(request, 'create-hotel.html', context=context)
