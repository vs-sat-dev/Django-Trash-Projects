from django.shortcuts import render

from .forms import HotelSearchForm


def hotels(request):
    if request.method == 'POST':
        pass
    else:
        form = HotelSearchForm()
        context = {'form': form}
        return render(request, 'hotels.html', context=context)
