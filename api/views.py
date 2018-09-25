import requests

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError
from rest_framework.authtoken.models import Token

from .serializers import CCUserSerializer
from .models import CCUser
from .utils import call_api

# Create your views here.


@api_view(['GET'])
def index(request):
    username = request.user.username if request.user.is_authenticated else "Guest"
    return Response("Hello {}!, welcome to Codechef Friends API".format(username))


@api_view(['GET'])
def search_users(request):
    query = request.query_params.get('q', None)
    users = CCUser.objects.filter(username__contains=query)
    serializer = CCUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def print_access_token(request):
    t = Token.objects.get(user=request.user)
    return Response({
        "username": request.user.username,
        "token": t.key
    })


@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
def friends(request):
    """
    GET
    -----
    - params  : None
    - returns : friend list
    PUT
    -----
    - params    :   username
    - returns   :   friend list
    """
    cc_user = request.user
    serializer = CCUserSerializer(cc_user.friends, many=True)

    if request.method == "GET":
        # nothing to do
        return Response(serializer.data)

    # rest of them require `username` in request.data
    if 'username' not in request.data:
        raise ParseError("Please provide username")

    friend_username = request.data['username']
    if cc_user.username == friend_username:
        raise ParseError("Please input a valid friend name")

    try:
        friend = CCUser.objects.get(username=friend_username)
    except ObjectDoesNotExist:
        # check if user has a account on codechef
        r = requests.head(
            "https://www.codechef.com/users/{}".format(friend_username))
        if r.status_code == 200:
            # create a new user
            friend = CCUser.objects.create(username=friend_username)
        elif r.status_code == 404:
            raise ParseError("Your friend is not on Codechef")
        else:
            raise APIException("Codechef ERROR")

    if request.method == "PUT":
        cc_user.friends.add(friend)

    return Response(serializer.data)


@api_view(['DELETE', 'GET'])
@permission_classes((IsAuthenticated,))
def get_friend_info(request, username=None):
    if request.method == "GET":
        userinfo = call_api("users", username, user=request.user, params={
            "fields": request.GET["fields"] if "fields" in request.GET else ""
        })
        return Response(userinfo)
    if request.method == "DELETE":
        try:
            friend = CCUser.objects.get(username=username)
            request.user.friends.remove(friend)
            # check if friend has token i.e. if he has ever logged in
            try:
                Token.objects.get(user=friend)
            except ObjectDoesNotExist:
                # if he's no-one's friend, remove him
                if len(friend.ccuser_set.all()) == 0:
                    # this user has no right to exists!!!
                    friend.delete()
            serializer = CCUserSerializer(request.user.friends, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise ParseError("He/She is not your friend.")
