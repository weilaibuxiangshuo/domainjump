from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,\
    AbstractBaseUser,PermissionsMixin,UserManager
from django.conf import settings

class NewUser(BaseUserManager):
    def _create_user(self,username,password,**kwargs):
        if not username:
            raise ValueError('The given username must be set')
        user=self.model(username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,username,password,**kwargs):
        kwargs['is_staff']=True
        kwargs['is_superuser']=False
        return self._create_user(username,password,**kwargs)

    def create_superuser(self,username,password,**kwargs):
        kwargs['is_staff']=True
        kwargs['is_superuser']=True
        return self._create_user(username,password,**kwargs)

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=32,unique=True,null=False)
    is_superuser = models.BooleanField(null=False,default=False)
    is_active = models.BooleanField(null=False,default=False)
    is_staff = models.BooleanField(null=False,default=False)
    mode =  models.CharField(max_length=32,null=True)
    number = models.IntegerField(null=True)
    target = models.CharField(max_length=256,null=True)
    last_login = None

    USERNAME_FIELD = 'username'
    objects=NewUser()

    def __str__(self):
        return self.username

    class Meta:
        db_table="system_user"



class Jump(models.Model):
    name=models.CharField(max_length=256,null=True)
    jumptarget=models.CharField(max_length=256,null=True,blank=True)
    is_jump=models.BooleanField(null=False,default=False)
    relationship=models.ForeignKey(to=settings.AUTH_USER_MODEL,null=True,related_name="jump_target",on_delete=models.CASCADE)
    class Meta:
        db_table="jump"
        ordering=["-id"]

