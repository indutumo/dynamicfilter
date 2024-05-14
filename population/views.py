from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from .models import  Population
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum, Avg, F, Q
from datetime import date
from django.contrib.auth.decorators import login_required
    

def is_valid_queryparam(param):
    return param != '' and param is not None


def population_list(request):
    login_url = '/'
    qs = Population.objects.order_by('-year')

    name = request.GET.get('name')
    year = request.GET.get('year')

    request.session['name'] = name
    request.session['year'] = year
    print(request.session['name'])

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

    request.session['name'] = name
    request.session['year'] = year

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


def population_list_pdf(request):
    login_url = '/'
    template_path = 'population_list_pdf.html'
    qs = Population.objects.order_by('-year')

    if 'name' in request.session:
        name = request.session['name']
    else:
        name = None

    if 'year' in request.session:
        year = request.session['year']
    else:
        year = None

    if is_valid_queryparam(name):
        qs = qs.filter(name__icontains=name)

    if is_valid_queryparam(year):
        qs = qs.filter(year__icontains=year)

    today = date.today()
    population = qs.aggregate(Sum('value'))['value__sum']
    context = {'population_list':qs,'population':population,'today':today}
    response = HttpResponse(content_type='application/pdf')
    if name is None:
        response['Content-Disposition'] = 'filename="World Population.pdf"'
    elif name:
        response['Content-Disposition'] = 'filename='+ str(name.capitalize()) + " " + str("Population.pdf")
    elif year:
        response['Content-Disposition'] = 'filename='+ str(year) + " " + str("World Population.pdf")

    # Find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
