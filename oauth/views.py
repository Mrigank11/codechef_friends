import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .utils import exchange_tokens, get_oauth_url
from api.models import CCUser
from api.utils import call_api

import os
# TODO: remove this in production
# This allows us to use a plain HTTP oauth_callback
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"


def index(request):
    return HttpResponse("Hello from OAuth!")


def oauth_redirect(request):
    state = "NONE"
    if "next" in request.GET:
        state = request.GET["next"]
    authorization_url = get_oauth_url(state=state)
    return redirect(authorization_url)


@api_view(['GET'])
def oauth_callback(request):
    tokens = exchange_tokens(request)
    if not tokens:
        raise APIException("error exchanging tokens")
    # fetch username from codechef
    response_map = call_api("users", "me", tokens=tokens)

    username = response_map["username"]
    # create a user in our DB if nout found
    try:
        cc_user = CCUser.objects.get(username=username)
    except ObjectDoesNotExist:
        cc_user = CCUser.objects.create(username=username)

    cc_user.tokens = json.dumps(tokens)
    cc_user.save()
    t, _ = Token.objects.get_or_create(user=cc_user)
    # login this fella
    login(request, cc_user)
    state = request.GET["state"]
    if state != "NONE":
        return redirect(state)
    return Response({'token': t.key, 'username': username})
