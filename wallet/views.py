import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

from .models import Wallets, UserProfile, Deposits as DepositsModel, Withdrawals as WithdrawalsModel
from .serializers import *

# Create your views here.


class Initialize(APIView):
    serializer_class = CustomeridSerializer

    def get(self):
        content = {'message': 'Initialize Account'}
        return Response(content)
    
    def post(self, request):
        customer_xid = request.data.get('customer_xid')
        try:
            userprofile = UserProfile.objects.get(customer_xid=customer_xid)
        except ObjectDoesNotExist:
            return Response('Not a valid customer id.')
        token, created = Token.objects.get_or_create(user=userprofile.user)
        return Response({
            "data": {
                "token": str(token)
            },
            "status": "success"
            })


class Wallet(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletsSerializer
    def get(self, request):
        status_choices = {'EN': 'enabled', "DS": 'disabled'}
        user = UserProfile.objects.get(user=request.user)
        wallet = Wallets.objects.get(owned_by=user)
        if wallet.status == 'EN':
            return Response({
                "data": {
                    "wallet": {
                        "id": wallet.id,
                        "owned_by": str(wallet.owned_by.customer_xid),
                        "status": status_choices[wallet.status],
                        "enabled_at": wallet.enabled_at,
                        "balance": int(wallet.balance)
                    }
                },
                "status": "success"
            })
        else:
            return Response('Wallet was disabled')

    def post(self, request):
        user = UserProfile.objects.get(user=request.user)
        status_choices = {'EN':'enabled',"DS":'disabled'}
        wallet = {
                    "owned_by": user,
                    "status": 'EN',
                    "enabled_at": datetime.datetime.now(),
                }
        wallet, _ = Wallets.objects.get_or_create(wallet)
        wallet.status = 'EN'
        wallet.enabled_at = datetime.datetime.now()
        wallet.save()
        return Response({
            "data": {
                "wallet": {
                    "id": wallet.id,
                    "owned_by": str(wallet.owned_by.customer_xid),
                    "status": status_choices[wallet.status],
                    "enabled_at": wallet.enabled_at,
                    "balance": int(wallet.balance)
                }
            },
            "status": "success"
            })

    def patch(self, request, *args, **kwargs):
        status_choices = {'EN': 'enabled', "DS": 'disabled'}
        user = UserProfile.objects.get(user=request.user)
        wallet = Wallets.objects.get(owned_by=user)
        if request.data.get('is_disabled') == 'true':
            wallet.status = 'DS'
            wallet.disabled_at = datetime.datetime.now()
            wallet.save()
            return Response({
                "data": {
                    "wallet": {
                        "id": wallet.id,
                        "owned_by": str(wallet.owned_by.customer_xid),
                        "status": status_choices[wallet.status],
                        "disabled_at": wallet.disabled_at,
                        "balance": int(wallet.balance)
                    }
                },
                "status": "success"
            })
        return Response("wrong parameters")


class Deposits(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = UserProfile.objects.get(user=request.user)
        wallet = Wallets.objects.get(owned_by=user)
        if wallet.status == 'EN':
            try:
                DepositsModel.objects.get(reference_id=request.data.get('reference_id'))
                return Response('Reference id already exist')
            except ObjectDoesNotExist:
                deposits = DepositsModel.objects.create(
                    deposited_by=user,
                    reference_id=str(request.data.get('reference_id')),
                    deposited_at=datetime.datetime.now(),
                    amount=int(request.data.get('amount'))
                )
                wallet.deposited_reference_id = deposits
                wallet.balance = int(wallet.balance) + int(request.data.get('amount'))
                wallet.save()
                return Response({
                    "data": {
                        "wallet": {
                            "id": wallet.id,
                            "deposited_by": str(wallet.deposited_reference_id.deposited_by),
                            "status": 'success',
                            "deposited_at": wallet.deposited_reference_id.deposited_at,
                            "amount": int(wallet.deposited_reference_id.amount),
                            "reference_id": str(wallet.deposited_reference_id.reference_id),
                        }
                    },
                    "status": "success"
                })
        else:
            return Response('Wallet was disabled')


class Withdrawals(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = UserProfile.objects.get(user=request.user)
        wallet = Wallets.objects.get(owned_by=user)
        if wallet.status == 'EN':
            if int(wallet.balance) < int(request.data.get('amount')):
                return Response('Insufficient Balance')
            try:
                WithdrawalsModel.objects.get(reference_id=request.data.get('reference_id'))
                return Response('Reference id already exist')
            except ObjectDoesNotExist:
                withdrawals = WithdrawalsModel.objects.create(
                    withdrawn_by=user,
                    reference_id=str(request.data.get('reference_id')),
                    withdrawn_at=datetime.datetime.now(),
                    amount=int(request.data.get('amount'))
                )
                wallet.withdrawn_reference_id = withdrawals
                wallet.balance = int(wallet.balance) - int(request.data.get('amount'))
                wallet.save()
                return Response({
                    "data": {
                        "wallet": {
                            "id": wallet.id,
                            "withdrawn_by": str(wallet.withdrawn_reference_id.withdrawn_by),
                            "status": 'success',
                            "withdrawn_at": wallet.withdrawn_reference_id.withdrawn_at,
                            "amount": int(wallet.withdrawn_reference_id.amount),
                            "reference_id": wallet.withdrawn_reference_id.reference_id,
                        }
                    },
                    "status": "success"
                })
        else:
            return Response('Wallet was disabled')

