from django.shortcuts import render
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User


class SnippetList(generics.ListAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    # serializerのcreateメソッドに'owner'が渡される => snippetの作成時にUser(外部キー)を関連付ける
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer