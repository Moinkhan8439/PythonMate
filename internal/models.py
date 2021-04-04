import jwt
from datetime import datetime ,timedelta
import time
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.conf import settings
# Create your models here.

class MyUserManager(UserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given  email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)
 
 



class MyUser(AbstractUser):
    email = models.EmailField( unique=True)
    username=models.CharField(max_length=50,null=True,blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name',]

    objects=MyUserManager()

    @property
    def token(self):
        now=datetime.now() + timedelta(days=2)
        token= jwt.encode({
           'email':self.email,
           'expiry': int(time.mktime(now.timetuple()))
        },
           settings.SECRET_KEY,
           algorithm='HS256'
        )
        return token
    
    def __str__(self):
        return self.email




class Client(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=("User"), on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


def client_post_save_user(sender,instance,created,*args,**kwargs):
    print(created)
    if created:
        c=Client.objects.create(user=instance)
        c.save()

post_save.connect(client_post_save_user,sender=MyUser)




class Shift(models.Model):
    Repeat_choices=[
        ('None','None'),
        ('Daily','Daily'),
        ('Weekly','Weekly')
    ]
    shift_choices=[
        ('Morning Shift - 5am to 9am','Morning Shift - 5am to 9am')
    ]
    start_date=models.DateField(verbose_name="Shift start date", auto_now=False, auto_now_add=False)
    arrival_time=models.TimeField(verbose_name="Shift start time", auto_now=False, auto_now_add=False)
    departure_time=models.TimeField(verbose_name="Shift end time", auto_now=False, auto_now_add=False)
    repeat=models.CharField(verbose_name="Select Repeat Type",choices=Repeat_choices ,max_length=10,default='None')
    shift_availability=models.CharField(verbose_name="Select shift",choices=shift_choices, max_length=50,default='Morning Shift - 5am to 9am')
    monday=models.BooleanField(verbose_name='Mon',default=False)
    tuesday=models.BooleanField(verbose_name='Tue',default=False)
    wednesday=models.BooleanField(verbose_name='Wed',default=False)
    thrusday=models.BooleanField(verbose_name='Thr',default=False)
    friday=models.BooleanField(verbose_name='Fri',default=False)
    saturday=models.BooleanField(verbose_name='Sat',default=False)
    sunday=models.BooleanField(verbose_name='Sun',default=False)
    client=models.ForeignKey(MyUser, verbose_name=("Shift Created By"), on_delete=models.CASCADE)

    def get_client_email(self):
        return self.client.email


