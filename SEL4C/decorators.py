from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def only_superadmins(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser == True:
            return view_func(request, *args, **kwargs)
        else:
            messages.success(request, "Acceso no autorizado")
            return redirect('index')
    return wrapper_func
