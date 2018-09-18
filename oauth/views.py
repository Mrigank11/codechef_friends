from django.http import HttpResponse
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session

import os
# TODO: remove this in production
# This allows us to use a plain HTTP callback
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

CLIENT_ID = 'd76c69dcf7e9dfeecb85f47d4abf8713'
CLIENT_SECRET = '39263da02c23967fe45dee1e6a2b432a'
REDIRECT_URI = 'http://127.0.0.1:8080/oauth/callback'

oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
authorization_url, _ = oauth.authorization_url('https://api.codechef.com/oauth/authorize', state="")

def index(request):
    return HttpResponse("Hello from OAuth!")

def oauth_redirect(request):
    return redirect(authorization_url)

def callback(request):
    # TODO: fix this
    # Codechef is not sending the standard oauth response!
    token = oauth.fetch_token(
        'https://api.codechef.com/oauth/token',
        code = request.GET['code'],
        client_secret=CLIENT_SECRET)
    print(token)
