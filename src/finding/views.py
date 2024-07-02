from django.shortcuts import render
from .models import Vacancy


def home_view(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'scrapping/home_vacans.html',
                  {'object_list': vacancies})
