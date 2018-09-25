import requests
import json

from django.contrib.auth import login

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api.models import CCUser
from api.utils import call_api

CLIENT_ID = 'd76c69dcf7e9dfeecb85f47d4abf8713'
CLIENT_SECRET = '39263da02c23967fe45dee1e6a2b432a'
REDIRECT_URI = 'http://127.0.0.1:8080/oauth/callback'


def recieve_tokens(request):
    code = request.GET['code']
    # exchange code for tokens
    r = requests.post("https://api.codechef.com/oauth/token",
                      json={
                          "grant_type": "authorization_code",
                          "code": code,
                          "client_id": CLIENT_ID,
                          "client_secret": CLIENT_SECRET,
                          "redirect_uri": REDIRECT_URI
                      },
                      headers={'content-Type': 'application/json'})
    response = r.json()
    if response["status"] != "OK":
        # TODO: exceptions
        return False
    tokens = response['result']['data']
    return tokens

def get_oauth_url():
    return f"https://api.codechef.com/oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state=xyz"

def handle_new_tokens(tokens, request):
    # fetch username from codechef
    response_map = call_api("users","me",tokens=tokens)

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
    return Response({'token': t.key, 'username': username})

