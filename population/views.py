from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from .models import  Population
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    

def is_valid_queryparam(param):
    return param != '' and param is not None


def population_list(request):
    login_url = '/'
    qs = Population.objects.order_by('-year')
    

    name = request.GET.get('name')
    year = request.GET.get('year')

    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)

    if is_valid_queryparam(year):
        qs = qs.filter(year__icontains=year)

    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 30)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    year_list = Population.objects.values_list('year', flat=True).order_by('year').distinct()
    country_list = Population.objects.values_list('name', flat=True).order_by('name').distinct()

    print(year_list)

    context = {
        'population_list': qs,
        'year_list':year_list,
        'country_list':country_list,
        'year':year,
        'name':name,
    }
    return render(request, "population_list.html", context)


def population_filter(request):
    login_url = '/'
    qs = Population.objects.order_by('-year')
    

    name = request.GET.get('name')
    year = request.GET.get('year')

    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)

    if is_valid_queryparam(year):
        qs = qs.filter(year__icontains=year)

    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 30)

    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'population_list': qs,
        'year':year,
        'name':name,
    }
    return render(request, "population_filter.html", context)