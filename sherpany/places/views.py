from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from urllib import urlencode
from urllib2 import Request , urlopen, HTTPError
import urllib, urllib2
import json


# Importing Models
from places.models import Place, FusionPlace

# 
# Home Page
#
def index(request):

	return TemplateResponse(request, 'index.html', {})

# 
# Method to created a new Place. It makes a validation that the locations
# does not exists in the Fusion Table.
#
@csrf_exempt
def add(request):

	place = Place()
	place.latitude = request.POST.get("latitude", 0)
	place.longitude = request.POST.get("longitude", 0)
	place.address = request.POST.get("address", "--1")

	fusion = FusionPlace()
	if (fusion.addressExists(place) == True):
		return JsonResponse({'status':'error', 'message' : 'address already exists!'})
	else:
		place.save()
		fusion.addPlace(place)
		return JsonResponse({'status':'ok', 'message': 'address inserted!'})

#
# Method to list all the items in the fusion table.
#
def all(request):
	fusion = FusionPlace()
	places = fusion.loadAll()
	items = []

	for p in places:
		items.append({'id': p[0], 'latitude': p[1], 'longitude': p[2], 'address': p[3]})

	return JsonResponse({'status':'ok', 'items': items})

#
# Method to delete all the items in the database and the fusion table.
#
def clear(request):

	fusion = FusionPlace()
	places = fusion.removeAll()
	
	Place.objects.all().delete()

	return JsonResponse({'status':'ok', 'message': "all points were deleted!"})