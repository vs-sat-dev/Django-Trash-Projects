from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
            ).order_by('-sort_date')

            p = Paginator(hotels_found, 20)
            page = request.GET.get('page')
            hotels_paginated = p.get_page(page)

            context = {'form': form, 'hotels': hotels_paginated, 'category': form.data['category'],
                       'text': form.data['text'], 'city': form.data['city']}
            return render(request, 'hotels.html', context=context)
    else:

        """import random
        authors = ['admin', 'chuvak']
        categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']
        facilities = ['Facilities 1', 'Facilities 2', 'Facilities 3']
        states = ['State 1', 'State 2', 'State 3']
        regions = ['Region 1', 'Region 2', 'Region 3']
        cities = ['City 1', 'City 2', 'City 3']
        for i in range(10000):
            author = User.objects.get(username=random.choice(authors))
            category = Category.objects.get(category=random.choice(categories))
            facility = Facilities.objects.get(facilities=random.choice(facilities))
            state = State.objects.get(state=random.choice(states))
            region = Region.objects.get(region=random.choice(regions))
            city = City.objects.get(city=random.choice(cities))
            Hotel.objects.create(title=f'Title {i}', description=f'Description of the hotel {i}', price=i*10,
                                 slug=f'title-{i}', author=author,
                                 category=category, facilities=facility, state=state, region=region, city=city,
                                 street=f'Street {i}', house=f'House {i}', adress=f'Street {i} House {i}',
                                 coord_x=float(i*0.01), coord_y=float(100.0 - i*0.01))"""

        form = HotelSearchForm()
        category = request.GET.get('category')
        text = request.GET.get('text')
        city = request.GET.get('city')

        category = category if category else ''
        text = text if text else ''
        city = city if city else ''

        p = Paginator(Hotel.objects.filter(
            Q(category__category__icontains=category) &
            Q(city__city__icontains=city) &
            (Q(description__icontains=text) |
             (Q(title__icontains=text)))
        ).order_by('-sort_date'), 20)
        page = request.GET.get('page')
        hotels_paginated = p.get_page(page)
        context = {'form': form, 'hotels': hotels_paginated, 'category': category, 'text': text, 'city': city}
        return render(request, 'hotels.html', context=context)


def hotel_detail(request, city, category, slug):
    """hotel = Hotel.objects.filter(Q(city__city=city),
                                 Q(category__category=category),
                                 Q(title=title)).first()"""
    hotel = get_object_or_404(Hotel, city=City.objects.get(city=city),
                              category=Category.objects.get(category=category), slug=slug)
    context = {'hotel': hotel}
    return render(request, 'hotel-detail.html', context=context)


@login_required(login_url='accounts:login')
def create_hotel(request):
    if request.method == 'POST':
        form = CreateHotelForm(data=request.POST, files=request.FILES, initial={'author': request.user.id})
        if form.is_valid():
            data = form.save()
            category = data.category
            city = data.city
            slug = data.slug

            """Hotel.objects.create(
                title=form.data['title'], image=form.files['image'], price=form.data['price'],
                description=form.data['description'], author=request.user,
                category=Category.objects.get(category=form.data['category']),
                state=State.objects.get(state=form.data['state']),
                region=Region.objects.get(region=form.data['region']),
                city=city.objects.get(city=form.data['city']),
                facilities=Facilities.objects.get(facilities=form.data['facilities']),
                street=form.data['street'], house=form.data['house'], adress=form.data['adress'],
                coord_x=form.data['coord_x'], coord_y=form.data['coord_y']
            )"""

            return redirect(f'hotel-detail/{city}/{category}/{slug}')
        else:
            context = {'form': form, 'message': form.errors}
            return render(request, 'create-hotel.html', context=context)
    else:
        form = CreateHotelForm(initial={'author': request.user})
        context = {'form': form}
        return render(request, 'create-hotel.html', context=context)
