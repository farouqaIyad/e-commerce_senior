from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import requests

# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut

# class get_location(APIView):

#     def get(self, request, format=None):
#         try:
#             geolocator = Nominatim(user_agent="geoapiExercises")

#             # Get current location using GPS coordinates
#             location = geolocator.geocode("me", timeout=10)

#             if location:
#                 return Response({"latitude":location.latitude,"lon":location.longitude})

#                 print("Address:", location.address)
#             else:
#                 return Response({"message":"location not found"})
#         except GeocoderTimedOut:
#             return Response({"message":"service timed out"})
