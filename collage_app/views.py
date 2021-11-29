from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from random import randint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework import generics
import time
from rest_framework.permissions import IsAdminUser
from .serializers import TokenSerializer, TokenUpdateSerializer, CollectionSerializer, UserSerializers
from .models import Token, Serie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

#
# class IsSuperUser(IsAdminUser):
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_superuser)


class TokenList(APIView):

    def get(self, request, format=None):
        token = Token.objects.filter(serie__choices="SOLD").order_by('?')
        time.sleep(10)
        serializer = TokenSerializer(token, many=True)
        return Response(serializer.data)


class SeriedToken(ModelViewSet):
    queryset = Token.objects.filter(status="SOLD")
    serializer_class = TokenSerializer

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        # serie_slug = self.kwargs['pk']
        return self.get_queryset()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Serie.DoesNotExist, KeyError):
            return Response({"error": "Requested Movie does not exist"}, status=HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TokenAddSet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.get('items', request.data)
        many = isinstance(data, list)
        print(data, many)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            # status=status.HTTP_201_CREATED,
            headers=headers
        )


class TokenRandomGet(ModelViewSet):
    queryset = Token.objects.filter(status="ACTIVE")
    serializer_class = TokenSerializer

    def get_queryset(self):
        i = randint(0, Token.objects.filter(status="ACTIVE").count() - 1)
        return self.queryset[i]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class TokenUpdateSet(ModelViewSet):
    queryset = Token.objects.filter(status="ACTIVE")
    serializer_class = TokenUpdateSerializer

    def create(self, request, *args, **kwargs):
        self.token_id = request.data.get('token_id', request.data)
        Token.objects.filter(token_id=self.token_id).update(status="SOLD")
        return Response()


class CollectionsGet(ModelViewSet):
    queryset = Token.objects.all().distinct("collection_id")
    serializer_class = CollectionSerializer

    def get_queryset(self):
        amount = Token.objects.filter(status="ACTIVE").count()
        if amount == 0:
            return self.queryset
        else:
            return {}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TokensGet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    def get_queryset(self):
        return self.queryset.filter(collection_id=self.coll_id)

    def create(self, request, *args, **kwargs):
        print(request.data)
        self.coll_id = request.data.get('collection_id', request.data)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class UserCheckGet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def create(self, request, *args, **kwargs):
        print(request.data)
        self.username = request.data.get('username', request.data)
        self.password = request.data.get('password', request.data)
        user = authenticate(username=self.username,
                            password=self.password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response("True")
            else:
                return Response("Success")
        else:
            return Response("Invalid login")