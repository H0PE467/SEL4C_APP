from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# CLASS FOR AUTHENTICATION
class CustomUserManager(BaseUserManager):

    # Normal Manager
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # Super Manager
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# MANAGERS
class manager(AbstractBaseUser, PermissionsMixin):
    # Required variables
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cellphone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)

    # Permission variable
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False) # Grants the ability to administer other maangers
    is_staff = models.BooleanField(default=False) # Grants the ability to log in the admin site

    # Authentication
    objects = CustomUserManager()

    # Username for Login
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email' 
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split('@')[0]

    # Name convention in admin
    def __str__(self):
        return self.email

# ACTIVITIES FROM USERS
class actInitial(models.Model):
    # An array of numbers from 1 to 5 (both inclusive), stored as a string due to storage easiness
    listOfAnswers = models.CharField(max_length=255, null=True, blank=True)

class act1(models.Model):
    ideas1 = models.CharField(max_length=255, null=True, blank=True)
    ideas2 = models.CharField(max_length=255, null=True, blank=True)
    ideas3 = models.CharField(max_length=255, null=True, blank=True)
    ideas4 = models.CharField(max_length=255, null=True, blank=True)
    ideas5 = models.CharField(max_length=255, null=True, blank=True)
    interview = models.TextField(null=True, blank=True)
    evidence = models.ImageField(upload_to='images/', null=True, blank=True)

class act2(models.Model):
    ODSideas1 = models.PositiveSmallIntegerField(null=True, blank=True)
    ODSideas2 = models.PositiveSmallIntegerField(null=True, blank=True)
    ODSideas3 = models.PositiveSmallIntegerField(null=True, blank=True)
    ODSideas4 = models.PositiveSmallIntegerField(null=True, blank=True)
    ODSideas5 = models.PositiveSmallIntegerField(null=True, blank=True)
    consequences1 = models.CharField(max_length=255, null=True, blank=True)
    consequences2 = models.CharField(max_length=255, null=True, blank=True)
    consequences3 = models.CharField(max_length=255, null=True, blank=True)
    consequences4 = models.CharField(max_length=255, null=True, blank=True)
    consequences5 = models.CharField(max_length=255, null=True, blank=True)
    problem = models.CharField(max_length=255, null=True, blank=True)
    causes1 = models.CharField(max_length=255, null=True, blank=True)
    causes2 = models.CharField(max_length=255, null=True, blank=True)
    causes3 = models.CharField(max_length=255, null=True, blank=True)

class act3(models.Model):
    reflection = models.TextField( null=True, blank=True)

class act4(models.Model):
    # Stores only Youtube Links
    link = models.CharField(max_length=510, null=True, blank=True)

class actFinal(models.Model):
    # Stores only Youtube Links
    link = models.CharField(max_length=510, null=True, blank=True)

# USERS FROM MOBILE APP
class user(models.Model):
    # Required variables
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=100)
    institution = models.CharField(max_length=255)
    academic = models.CharField(max_length=255)
    discipline = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    gender = models.CharField(max_length=15)

    # Optional variables
    appRating = models.PositiveSmallIntegerField(blank=True, null=True, default = 3)


    # Automated variables
    progress = models.PositiveSmallIntegerField(default = 0)
    currentActivity = models.PositiveSmallIntegerField(default = 0)

    # Foreign keys for activities associated
    actInit = models.ForeignKey(actInitial, on_delete=models.SET_NULL, null=True, blank=True)
    act1ID = models.ForeignKey(act1, on_delete=models.SET_NULL, null=True, blank=True)
    act2ID = models.ForeignKey(act2, on_delete=models.SET_NULL, null=True, blank=True)
    act3ID = models.ForeignKey(act3, on_delete=models.SET_NULL, null=True, blank=True)
    act4ID = models.ForeignKey(act4, on_delete=models.SET_NULL, null=True, blank=True)
    actFinal = models.ForeignKey(actFinal, on_delete=models.SET_NULL, null=True, blank=True)

    # Name convention in admin
    def __str__(self):
        return self.name
