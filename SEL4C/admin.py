from django.contrib import admin

# Register your models here.


from .models import *


myModels = [user, manager, actInitial, act1, act2, act3, act4, actFinal]

admin.site.register(myModels)