from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


# Stops admins without the is_superuser attribute from accessing the view
def only_superadmins(view_func):
    def wrapper_func(request, *args, **kwargs):

        # Get user of the session information and attributes
        if request.user.is_superuser == True:

            # Successful
            return view_func(request, *args, **kwargs)
        else:
            # Redirect
            messages.success(request, "Acceso no autorizado")
            return redirect('index')
        

    return wrapper_func
