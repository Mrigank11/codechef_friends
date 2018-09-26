import os
import requests
import json
import logging

logger = logging.getLogger(__name__)

API_URL = 'https://api.codechef.com'


def call_api(*path, params=None, user=None, tokens=None):
    if not tokens:
        tokens = json.loads(user.tokens)
    # set apporipriate headers
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(tokens['access_token'])
    }
    # buid complete path from pieces `path`
    compiled_path = "/".join([str(part) for part in path])

    url = "{}/{}".format(API_URL, compiled_path)

    logger.debug("calling {}, params: {}".format(url, params))
    response = requests.get(url, headers=headers, params=params)
    response_map = response.json()
    logger.debug("response from CC: {}".format(response_map))

    if response_map['status'] == "OK":
        return response_map["result"]["data"]["content"]
    else:
        logger.debug("status not OK, result: {}".format(
            response_map["result"]))
        # check if error is unauthorized
        if response_map["result"]["errors"][0]["code"] == "unauthorized":
            logger.debug("tokens expired, trying to refresh tokens")
            resp = requests.post("{}/oauth/token".format(API_URL),
                                 json={"grant_type": "refresh_token",
                                       "refresh_token": tokens["refresh_token"],
                                       "client_id": os.environ["CC_CLIENT_ID"],
                                       "client_secret": os.environ["CC_CLIENT_SECRET"]
                                       },
                                 headers={'content-Type': 'application/json'})
            resp_map = resp.json()
            logger.debug("response from CC: ", resp_map)
            # store tokens
            if resp_map["status"] == "OK":
                tokens = resp_map["result"]["data"]
                if user:
                    # update this user's tokens
                    user.tokens = json.dumps(tokens)
                    user.save()
                # re-run the query
                logger.debug("retrying query with new tokens")
                return call_api(*path, params=params, user=user, tokens=tokens)
            else:
                # TODO:seperate exception?
                raise Exception(resp_map)
        else:
            err = response_map['result']['errors'][0]
            raise Exception('Message: {}, Code: {}'.format(
                err['message'], err['code']))
