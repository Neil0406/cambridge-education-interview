from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from common.enum import Gender
from common.helperfunc import normalize_phone_number

class UserAccountManager(BaseUserManager):
    def create_user(self, phone, password, **kwargs):
        """ Create a new user profile """
        if not phone:
            raise ValueError('User must have an phone')
        phone = normalize_phone_number(phone)
        user = self.model(phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
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
    
    def update_user(self, user_id, phone=None, name=None, password=None):
        """ Update user profile """
        user = UserAccount.objects.get(id=user_id)
        if password != None and password.strip() != '':
            user.password = password
            user.set_password(user.password)
        if phone:
            user.email = phone
        if name:
            user.name = name
        user.updated_at = datetime.now()
        user.save()
        
    def delete_user(self, user_id):
        user = UserAccount.objects.get(id=user_id)
        if user.is_superuser != True:
            user.is_delete = True
            user.save()
            
    def update_password(self, user_id, password=None):
        user = UserAccount.objects.get(id=user_id)
        if password != None and password.strip() != "":
            user.password = password
            user.set_password(user.password)
            user.updated_at = datetime.now()
            user.save()
        return user.id
    
    
class UserAccount(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(unique=True, null=False, blank=False, max_length=255, verbose_name='電話')
    email = models.EmailField(null=True, blank=False, max_length=255, verbose_name='Email')
    name = models.CharField(null=True, blank=False, max_length=255, verbose_name='姓名')
    gender = models.IntegerField(choices=[(tag.value, tag.label) for tag in Gender], null=True, blank=False, verbose_name='性別')
    birthday = models.DateTimeField(null=True, blank=False, auto_now_add=False, verbose_name='生日')
    picture = models.CharField(null=True, blank=False,max_length=255, verbose_name='照片')
    location = models.CharField(null=True, blank=False,max_length=255, verbose_name='位置')
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
    
