from rest_framework import serializers
from .models import Serie, Token
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class TokenUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            'token_id',
            'status'
        ]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            'collection_id'
        ]


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
