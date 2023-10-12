from django.db import models


class manager(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    cellphone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    password_confirmation = models.CharField(max_length=128)
    isSuperAdmin = models.BooleanField()

    def __str__(self):
        return self.name

class actInicial(models.Model):
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
    link = models.CharField(max_length=510, null=True, blank=True)

class actFinal(models.Model):
    link = models.CharField(max_length=510, null=True, blank=True)

# Create your models here.
class user(models.Model):
    # Obligatorio
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=100)
    institution = models.CharField(max_length=255)
    academic = models.CharField(max_length=255)
    discipline = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    gender = models.CharField(max_length=15)

    # # Opcional
    appRating = models.PositiveSmallIntegerField(blank=True, null=True, default = 3)


    # # Cambiante
    progress = models.PositiveSmallIntegerField(default = 0)
    currentActivity = models.PositiveSmallIntegerField(default = 0)
    
    actInit = models.ForeignKey(actInicial, on_delete=models.SET_NULL, null=True, blank=True)
    act1ID = models.ForeignKey(act1, on_delete=models.SET_NULL, null=True, blank=True)
    act2ID = models.ForeignKey(act2, on_delete=models.SET_NULL, null=True, blank=True)
    act3ID = models.ForeignKey(act3, on_delete=models.SET_NULL, null=True, blank=True)
    act4ID = models.ForeignKey(act4, on_delete=models.SET_NULL, null=True, blank=True)
    actFinal = models.ForeignKey(actFinal, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
