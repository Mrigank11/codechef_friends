import os
import requests


def exchange_tokens(request):
    code = request.GET['code']
    # exchange code for tokens
    r = requests.post("https://api.codechef.com/oauth/token",
                      json={
                          "grant_type": "authorization_code",
                          "code": code,
                          "client_id": os.environ["CC_CLIENT_ID"],
                          "client_secret": os.environ["CC_CLIENT_SECRET"],
                          "redirect_uri": os.environ["CC_REDIRECT_URI"]
                      },
                      headers={'content-Type': 'application/json'})
    response = r.json()
    if response["status"] != "OK":
        # TODO: exceptions
        return False
    tokens = response['result']['data']
    return tokens


def get_oauth_url(state=""):
    return "https://api.codechef.com/oauth/authorize?response_type=code&client_id={}&redirect_uri={}&state={}".format(os.environ["CC_CLIENT_ID"], os.environ["CC_REDIRECT_URI"], state)
