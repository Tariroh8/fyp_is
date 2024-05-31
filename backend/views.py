from django.shortcuts import render
from backend.models import District, Animalcases
from django.core.serializers import serialize
from django.contrib.gis.serializers import geojson
from django.http import  HttpResponse
from django.http import JsonResponse
import json

def landing(request):
    context ={}
    return render(request, 'landing.html', context)


def index(request):
    districts = District.objects.all()
    serialized_districts = serialize('geojson', districts)
    cases = Animalcases.objects.all()
    serialized_cases = serialize('geojson', cases)

    context = {
        'districts': districts,
        'serialized_districts': serialized_districts,
        'serialized_cases':serialized_cases,
    }
    return render(request, 'index.html', context)

def district (request, name):
    district = District.objects.get(name_2 = name)
    context = {}
    context['district'] = district
    return render(request, 'district.html', context)










