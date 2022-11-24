from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from core import settings


class UserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,password):
        if not email:
            raise ValueError('El User debe tener un email')
        User = self.model(
            email = self.normalize_email(email),
            first_name = first_name ,
            last_name = last_name,
            password = password,
        )
        User.set_password(password)
        User.save()
        return User
    
    def create_superuser(self,email,first_name,last_name,password):
        User = self.model(
            email = email,
            first_name = first_name ,
            last_name = last_name,
            password = password,)
        User.User_administrador = True
        User.save()
        return User
    
class User(AbstractBaseUser):
    email = models.EmailField('Email',unique =True, max_length=254)
    first_name = models.CharField ('Nombre' ,max_length = 254)
    last_name = models.CharField ('Apellidos',max_length = 254) 
    is_lander = models.BooleanField('Es lender',default=False)
    is_borrower = models.BooleanField('Es borrower',default=False)
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    def __str__(self):
        return f'{self.first_name},{self.last_name}'
    def has_perm(self,perm,obj = None) :
        return True
    def has_module_perms(self,app_label):
        return True
    def get_full_name(self): 
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def is_staff(self):
        return self.User_administrador
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
        
class LenderProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField()  
    
    class Meta:
        verbose_name = 'LenderProfile'
        verbose_name_plural = 'LanderProfiles'

class BorrowerProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    need_money_for = models.CharField (max_length = 100, verbose_name = 'Need money for')
    description = models.CharField (max_length = 5000, unique = True, verbose_name = 'Description')
    amount_need = models.IntegerField(verbose_name = 'Amount need')
    class Meta:
        verbose_name = 'BorrowerProfile'
        verbose_name_plural = 'BorrowerProfiles'    
    
    

    