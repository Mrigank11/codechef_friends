from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from oauth.utils import get_oauth

from .serializers import CCUserSerializer
from .models import CCUser

# Create your views here.


@api_view(['GET'])
def index(request):
    username = request.user.username if request.user.is_authenticated else "Guest"
    return Response("Hello {}!, welcome to Codechef Friends API".format(username))


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def print_oauth_token(request):
    return Response({
        "username": request.user.username,
        "token": request.auth.key
    })


@api_view(['GET'])
def search_users(request):
    query = request.query_params.get('q', None)
    users = CCUser.objects.filter(username__contains=query)
    serializer = CCUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def friends(request):
    # TODO: better exception  handling
    # TODO: remove this hack
    cc_user = CCUser.objects.get(username=request.user.username)
    if request.method == "GET":
        friends = cc_user.friends
        serializer = CCUserSerializer(friends, many=True)
        return Response(serializer.data)
    elif request.method == "PUT":
        friend = CCUser.objects.get(username=request.data['username'])
        cc_user.friends.add(friend)
        serializer = CCUserSerializer(friend)
        return Response(serializer.data)
    elif request.method == "DELETE":
        friend = CCUser.objects.get(username=request.data['username'])
        cc_user.friends.remove(friend)
        serializer = CCUserSerializer(friend)
        return Response(serializer.data)
