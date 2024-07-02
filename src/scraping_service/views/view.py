import datetime

from django.shortcuts import render


def get_home_page(request):
    date = datetime.datetime.now().date()
    name = 'Alex'
    _context = {'name': name, 'date': date}
    return render(request, 'base.html', _context)
