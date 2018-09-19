from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError
from rest_framework.authtoken.models import Token

from oauth.utils import get_oauth

from .serializers import CCUserSerializer
from .models import CCUser

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


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def friends(request):
    cc_user = request.user
    if request.method == "GET":
        friends = cc_user.friends
        serializer = CCUserSerializer(friends, many=True)
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
        raise ParseError("Your friend is not on codechef friends")

    if request.method == "PUT":
        cc_user.friends.add(friend)

    if request.method == "DELETE":
        cc_user.friends.remove(friend)

    serializer = CCUserSerializer(friend)
    return Response(serializer.data)
