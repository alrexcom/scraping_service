from django.shortcuts import render


def get_home_page(request):
    return render(request, 'base.html',{'title':'Поиск ваканий'})
