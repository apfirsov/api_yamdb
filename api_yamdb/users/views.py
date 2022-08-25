from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import status, viewsets
from .serializers import (SignUpSerializer,
                          MyTokenObtainSlidingSerializer,
                          UserSerializer)
from django.contrib.auth.tokens import default_token_generator
from .models import User

from rest_framework_simplejwt.views import TokenViewBase


@api_view(['POST', ])
def sign_up_view(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(
                username=request.data['username']
            )
            send_confirmation_code(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    print('-------------')
    print(confirmation_code)
    print('-------------')


class MyTokenObtainSlidingView(TokenViewBase):
    serializer_class = MyTokenObtainSlidingSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(detail=False, methods=['GET', 'PATCH'], name='My information')
    def me(self, request, *args, **kwargs):
        me = User.objects.get(username=request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(me)
            return Response(serializer.data)
        serializer = self.get_serializer(
            me,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )