from django.shortcuts import render
from django.contrib.auth import authenticate,login

from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from rest_framework.generics import ListCreateAPIView

# Create your views here.
from .models import Client,MyUser , Shift
from .seriailizers import UserLoginSerializer , UserSerializer , ShiftSerializer


@api_view(['GET'])
def api_overview(request):
    url_list={
        
        'Register Client                                         '  :                 '/user-register/',
        'LOGIN                                                   '  :                 '/user-login/',
        'ADD-SHIFT                                               '  :                 '/add-shift/',
        'List of shift                                           '  :                 '/get-shift/',
                                                                     
    }

class UserView(ListCreateAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAdminUser]
    queryset=MyUser.objects.all()



class LoginView(APIView):
    serializer_class=UserLoginSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class ShiftView(ListCreateAPIView):
    serializer_class=ShiftSerializer
    permission_classes=[IsAuthenticated]
    queryset=Shift.objects.all()