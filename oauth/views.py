from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from api.models import CCUser
from .utils import recieve_tokens, get_oauth

import os
# TODO: remove this in production
# This allows us to use a plain HTTP oauth_callback
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"


def index(request):
    return HttpResponse("Hello from OAuth!")


def oauth_redirect(request):
    oauth = get_oauth()
    authorization_url, _ = oauth.authorization_url(
        'https://api.codechef.com/oauth/authorize', state="")
    return redirect(authorization_url)


@api_view(['GET'])
def oauth_callback(request):
    token = recieve_tokens(request)
    if not token:
        raise APIException("error exchanging tokens")

    oauth = get_oauth(token=token)
    # fetch username from codechef
    response_map = oauth.get("https://api.codechef.com/users/me").json()
    if response_map["status"] != "OK":
        return Response("Codechef error")

    username = response_map["result"]["data"]["content"]["username"]
    # create a user in our DB if nout found
    try:
        cc_user = CCUser.objects.get(username=username)
    except ObjectDoesNotExist:
        cc_user = CCUser.objects.create(username=username)

    t, _ = Token.objects.get_or_create(user=cc_user)
    # login this fella
    login(request, cc_user)
    return Response({'token': t.key, 'username': username})
