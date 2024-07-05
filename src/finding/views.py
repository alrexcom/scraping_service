from django.shortcuts import render

from . import utils
from .forms import FindForm
from .models import Vacancy


def home_view(request):
    # print(request.POST)
    # print(request.GET)
    form=FindForm()
    city = request.GET.get('city')
    _filter = {}
    if city:
        _filter['city__slug'] = utils.from_cyrillic_to_eng(city)

    language = request.GET.get('language')
    if language:
        _filter['language__slug'] = utils.from_cyrillic_to_eng(language)
    # queryset
    qs = Vacancy.objects.filter(**_filter)

    # vacancies = Vacancy.objects.all()
    return render(request, 'scrapping/home_vacans.html',
                  {'object_list': qs, 'form': form})
