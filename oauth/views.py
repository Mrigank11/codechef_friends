import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .utils import recieve_tokens, get_oauth_url, handle_new_tokens

import os
# TODO: remove this in production
# This allows us to use a plain HTTP oauth_callback
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"


def index(request):
    return HttpResponse("Hello from OAuth!")


def oauth_redirect(request):
    authorization_url = get_oauth_url()
    return redirect(authorization_url)


@api_view(['GET'])
def oauth_callback(request):
    tokens = recieve_tokens(request)
    if not tokens:
        raise APIException("error exchanging tokens")
    return handle_new_tokens(tokens, request)


@api_view(['POST'])
def cli_auth(request):
    tokens = request.data
    return handle_new_tokens(tokens, request)
