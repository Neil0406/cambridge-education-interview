from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from common.enum import Gender
from common.helperfunc import normalize_phone_number
import uuid

class UserAccountManager(BaseUserManager):
    def create_user(self, phone, password, **kwargs):
        """ Create a new user profile """
        if not phone:
            raise ValueError('User must have an phone')
        phone = normalize_phone_number(phone)
        user = self.model(phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        refresh = RefreshToken.for_user(user)
        return user, refresh
        
    def create_superuser(self, phone, name, password):
        """ Create a new superuser profile """
        if not phone:
            raise ValueError('User must have an phone')
        phone = normalize_phone_number(phone)
        user = self.model(phone=phone, name=name)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
# 帳號
class UserAccount(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(unique=True, null=False, blank=False, max_length=255, verbose_name='電話')
    email = models.EmailField(null=True, blank=False, max_length=255, verbose_name='Email')
    name = models.CharField(null=True, blank=False, max_length=255, verbose_name='姓名')
    gender = models.IntegerField(choices=[(tag.value, tag.label) for tag in Gender], null=True, blank=False, verbose_name='性別')
    birthday = models.DateTimeField(null=True, blank=False, auto_now_add=False, verbose_name='生日')
    picture = models.CharField(null=True, blank=False,max_length=255, verbose_name='照片')
    latitude = models.FloatField(null=True, blank=False, verbose_name='緯度')
    longitude = models.FloatField(null=True, blank=False, verbose_name='經度')
    is_staff = models.BooleanField(default=False, null=False, blank=False, verbose_name='管理員')
    is_active = models.BooleanField(default=True, null=False, blank=False,verbose_name='啟用帳號')
    is_superuser = models.BooleanField(default=False,  null=False, blank=False,verbose_name='超級使用者')
    is_delete = models.BooleanField(default=False, null=False, blank=False, verbose_name='軟刪除')
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False,verbose_name='建立日期')
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False,verbose_name='更新日期')
    objects = UserAccountManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']
    def __str__(self):
        return self.phone
    
# 偏好
class Hobby(models.Model):
    name = models.CharField(null=False, blank=False, max_length=256, verbose_name="偏好")
    def __str__(self):
        return "{}".format(self.name)
    
# 偏好mapping 
class HobbyMapping(models.Model):
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, verbose_name="偏好")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name="帳號")
    def __str__(self):
        return "{}".format(self.hobby)

# 興趣
class Interest(models.Model):
    name = models.CharField(null=False, blank=False, max_length=256, verbose_name="興趣")
    def __str__(self):
        return "{}".format(self.name)
    
# 興趣mapping
class InterestMapping(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, verbose_name="興趣")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name="帳號")
    def __str__(self):    
        return "{}".format(self.interest)

# 聊天室
class ChatrRoom(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")
    def __str__(self):
        return "{}".format(self.uuid)
    
# 聊天室mapping
class ChatrRoomMapping(models.Model):
    chatr_room = models.ForeignKey(ChatrRoom, on_delete=models.CASCADE, verbose_name="聊天室")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name="帳號")
    def __str__(self):
        return "{}".format(self.chatr_room)
    
