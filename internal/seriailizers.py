  
from rest_framework import serializers
from .models import Client , MyUser , Shift
from django.contrib.auth import authenticate,login
import jwt
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=MyUser
        fields=['email','first_name','last_name','password']
        extra_kwargs = {'password': {'write_only': True}}
    

    def create(self,validated_data):
        password=validated_data.pop('password')
        user=MyUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self,data):
        email = data.get('email', None)
        password = data.get('password', None)

        user=authenticate(username=email,password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password is not found.')

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        data['token']=user.token

        return data




class ShiftSerializer(serializers.ModelSerializer):
    days_of_week=[
        ("monday",'Mon'),
        ("tuesday",'Tue'),
        ("wednesday",'Wed'),
        ("thrusday",'Thr'),
        ("friday",'Fri'),
        ("saturday",'Sat'),
        ("sunday",'Sun'),
    ]

    shift_days=serializers.MultipleChoiceField(
        choices=days_of_week,
        required=False,
        write_only=True,
        help_text='press ctrl to select multiple.',
        )

    weekdays_only=serializers.BooleanField(write_only=True,
        required=False,
        default=False,
        )
    
    client_email=serializers.CharField(source='get_client_email')


    class Meta:
        model=Shift
        fields=['client','monday','tuesday','wednesday','thrusday','friday','saturday','sunday','start_date','arrival_time',
            'departure_time','repeat','shift_availability','shift_days','weekdays_only','client_email']
        read_only_fields=['client','monday','tuesday','wednesday','thrusday','friday','saturday','sunday','client_email']


    def validate(self,data):
        if(data['arrival_time'] > data['departure_time']):
            raise serializers.ValidationError('Shift end time should be after Shift start time.')
        if(data['weekdays_only'] is False and len(data['shift_days'])==0):
            raise serializers.ValidationError('Either select the days from the shift days or select weekdays only.')
        return data


    def create(self,validated_data):
        print(self.context['request'].user.email)
        client=self.context['request'].user
        week={
            'monday':False,
            'tuesday':False,
            'wednesday':False,
            'thrusday':False,
            'friday':False,
            'saturday':False,
            'sunday':False
        }

        if(validated_data['weekdays_only']==True):
            week['monday']=True
            week['tuesday']=True
            week['wednesday']=True
            week['thrusday']=True
            week['friday']=True
        else:
            for i in validated_data['shift_days']:
                week[i]=True

        validated_data.pop('weekdays_only')
        validated_data.pop('shift_days')
        s=Shift.objects.create(client=client,monday=week['monday'],tuesday=week['tuesday'],wednesday=week['wednesday'],
                thrusday=week['thrusday'],friday=week['friday'],saturday=week['saturday'],sunday=week['sunday'],**validated_data
            )
        return s


