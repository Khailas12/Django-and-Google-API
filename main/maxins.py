from humanfriendly import format_timespan
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.http import JsonResponse
import requests
import datetime
import json


# this handles the errors that are passed back to the AJAX calls
def FormErrors(*args):
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
def redirect_parms(**kwargs):
    url  = kwargs.get('url')
    parms = kwargs.get('parms')
    response = redirect(url)
    
    if parms:
        query_string = urlencode(parms)
        response['Location'] += '?' + query_string
        
    return response
    

# mixing it to the ajaxify form, can be over written in view by calling form_valid method
class AjaxFormMixin(object):

    def form_invalid(self, form):
        response = super(AjaxFormMixin).form_invalid(form)  # super is used to give acess to the parent or sibling class
        if self.request.is_ajax():
            message = FormErrors(form)
            return JsonResponse(
                {
                    'result': 'Error',
                    'message': message
                }
            )
        return response

    def form_valid(self, form):
        response = super(AjaxFormMixin).form_valid(form)
        if self.request.is_ajax():
            form.save()
            return JsonResponse(
                {
                    'result': 'Success',
                    'message': ''
                }
            )
        return response