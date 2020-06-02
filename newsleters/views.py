from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import NewsleterAccount

import json
import requests
from decouple import config

MAILCHIMP_API_KEY = config('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = config('MAILCHIMP_DATA_CENTER')
MAILCHIMP_EMAIL_LIST_ID = config('MAILCHIMP_EMAIL_LIST_ID')

api_url = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
members_endpoint = f'{api_url}/lists/{MAILCHIMP_EMAIL_LIST_ID}/members'


def subscribe_email(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }
    req = requests.post(
        members_endpoint,
        auth=("", MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return req.status_code, req.json()


def newsleter_email_list(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        email_query = NewsleterAccount.objects.filter(email=email)
        
        if email:
            if email_query.exists():
                messages.info(request, "You are already subscribed")
            else:
                try:
                    subscribe_email(email)
                    subscribed = NewsleterAccount.objects.create(email=email)
                    subscribed.save()
                    messages.success(request, "Subscribed succesfully")
                except:
                    messages.warning(request, "Failed to Subscribed")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "You didn't put a email")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
