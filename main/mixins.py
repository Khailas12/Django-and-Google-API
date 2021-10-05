from humanfriendly import format_timespan
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.http import JsonResponse
import requests
import datetime
import json


# this handles the errors that are passed back to the AJAX calls
def form_errors(*args):
    message = ""
    for f in args:
        if f.errors:
            message = f.errors.as_text()

    return message


def reCaptcha_validation(token):
    result = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token
        }
    )

    return result.json()


# this appends url parameters when redirecting users
def redirect_params(**kwargs):
    url = kwargs.get('url')
    params = kwargs.get('params')
    response = redirect(url)

    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string

    return response


# mixing it to the ajaxify form, can be over written in view by calling form_valid method
class AjaxFormMixin(object):

    def form_invalid(self, form):
        # super gives access to the parent of sibling class
        response = super(AjaxFormMixin).form_invalid(form)

        if self.request.is_ajax():
            message = form_errors(form)
            return JsonResponse(
                {
                    'result': 'Error',
                    'message': message
                }
            )
        return response

    def form_valid(self, form):
        response = super(AjaxFormMixin).form_valid(form)

        if response.is_ajax():
            form.is_valid()
            return JsonResponse(
                {
                    'result': 'Success',
                    'message': ''
                }
            )
        return response


def directions(*args, **kwargs):    # this handles direction from google
    # orign
    lat_a = kwargs.get('lat_a')     # latitude
    long_a = kwargs.get('long_a')   # longitude

    # destination
    lat_b = kwargs.get('lat_b')
    long_b = kwargs.get('long_b')

    # waypoints
    lat_c = kwargs.get('lat_c')
    long_c = kwargs.get('long_c')
    lat_d = kwargs.get('lat_d')
    long_d = kwargs.get('long_d')


    origin = f'{lat_a}, {long_a}'   # a demo of hw it looks 54.1,74.6
    destination = f'{lat_b}, {long_b}'
    waypoints = f'{lat_c}, {long_c}|{lat_d}, {long_d}'

    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params={
            'origin': origin,
            'destination': destination,
            'waypoints': waypoints,
            'key': settings.GOOGLE_API_KEY
        }
    )

    directions = result.json()


    if directions['status'] == 'OK':
        routes = directions['routes'][0]['legs']

        distance = 0
        duration = 0
        route_list = []

        for route in range(len(routes)):
            distance += int(routes[route]['distance']['value'])
            duration += int(routes[route]['duration']['value'])

            route_step = {
                'origin': routes[route]['start_address'],
                'destination': routes[route]['end_address'],

                'distance': routes[route]['distance']['text'],
                'duration': routes[route]['duration']['text'],

                'steps': [
                    [
                        s['distance']['text'],
                        s['duration']['text'],
                        s['html_instructions'],
                    ]

                    for s in routes[route]['steps']
                    
                ]
            }
            route_list.append(route_step)

    return {
        'origin': origin,
        'destination': destination,
        'distance': f'{round(distance/1000, 2)} Km',
        'duration': format_timespan(duration),
        'route': route_list
    }