from django.shortcuts import render
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from rest_framework import generics, renderers
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


# APIのルートのエンドポイント
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
    })


class SnippetViewSet(viewsets.ModelViewSet):
    """list, create, retrieve, update, destroyアクションを持つ"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    # actionデコレータを使用して標準のcreate, update, deleteスタイルに適合しないカスタムエンドポイントを定義
    # snippetコードをHTMLにレンダリングするため設定(tutorialに依存)
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    # serializerのcreateメソッドに'owner'が渡される => snippetの作成時にUser(外部キー)を関連付ける
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ReadOnlyModelViewSet => 読み取り専用
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """list, detailアクションを持つ"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
