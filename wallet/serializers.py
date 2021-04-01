from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class CustomeridSerializer(ModelSerializer):
    customer_xid = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = ("customer_xid", )


class WalletsSerializer(ModelSerializer):

    class Meta:
        model = Wallets
        fields = '__all__'