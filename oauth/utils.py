import requests

from requests_oauthlib import OAuth2Session

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


def get_oauth(token=None):
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, token=token)
    return oauth
