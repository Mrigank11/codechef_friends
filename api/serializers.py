from rest_framework import serializers

from .models import CCUser


class CCUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCUser
        fields = ('username',)
