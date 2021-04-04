from datetime import datetime
import time
import jwt

from .models import MyUser
from django.conf import settings

from rest_framework import authentication , exceptions


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self,request):
        auth_header=authentication.get_authorization_header(request).split()
        
        request.user=None

        if not auth_header:
            return None
        
        if len(auth_header)==1:
            return None
        
        elif len(auth_header)>2:
            return None
        
        prefix=auth_header[0].decode('utf-8')
        token=auth_header[1].decode('utf-8')

        if prefix != 'token':
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self,request,token):

        try:
            payload=jwt.decode(
                token,settings.SECRET_KEY,algorithms = ["HS256"]
            )
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user=MyUser.objects.get(email=payload['email'])
        except MyUser.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)


        now=datetime.now()
        now_secs=int(time.mktime(now.timetuple()))

        if int(payload['expiry']) < now_secs:
            msg = 'Token Expired.'
            raise exceptions.AuthenticationFailed(msg)
        
        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)
        
        return (user, token)