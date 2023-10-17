from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework import viewsets
from .serializer import *
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from django.db.models import Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from .decorators import *


# Create your views here.

def logoutUser(request):
    logout(request)
    return redirect('login')

def showLogin(request):

    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':

            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)


            if user is not None:
                login(request, user)
                return redirect('index')
            
            error_message = "Usuario o contraseña incorrectos. Intentelo de nuevo."
            return render(request, 'login.html', {'error_message':error_message})

        return render(request, 'login.html')

@login_required(login_url='login')
def showIndex(request):

    data = user.objects.all()  # Retrieve data from your database using your model
    average_rating = data.aggregate(avg_app_rating=Avg('appRating'))['avg_app_rating']
    peopleWhoHaventStarted = data.filter(currentActivity=0).count()
    peopleInDI = data.filter(currentActivity=1).count()
    peopleInAct1 = data.filter(currentActivity=2).count()
    peopleInAct2 = data.filter(currentActivity=3).count()
    peopleInAct3 = data.filter(currentActivity=4).count()
    peopleInAct4 = data.filter(currentActivity=5).count()
    peopleInEF = data.filter(currentActivity=6).count()

    return render(request, 'index.html',{
                                            'peopleWhoHaventStarted':peopleWhoHaventStarted,
                                            'peopleInDI':peopleInDI,
                                            'peopleInAct1':peopleInAct1,
                                            'peopleInAct2':peopleInAct2,
                                            'peopleInAct3':peopleInAct3,
                                            'peopleInAct4':peopleInAct4,
                                            'peopleInEF':peopleInEF,
                                            'average_rating': average_rating
    } )


# MANAGERS
@login_required(login_url='login')
@only_superadmins
def showManagers(request, page):
    start  = ((page-1)*100)
    end  = 99 + ((page-1)*100)
    data = manager.objects.all()[start:end]  # Retrieve data from your database using your model

    if(page == 1):
        pagePrev = 1
        pageCurr = 1
        pageNext = 2
        pageFirst = 1
        pageSecond = 2
        pageThird = 3
    else:
        pagePrev = page-1
        pageCurr = page
        pageNext = page+1
        pageFirst = pagePrev
        pageSecond = pageCurr
        pageThird = pageNext

    return render(request, 'managers.html', {
                                            'data': data, 
                                            'pagePrev':pagePrev,
                                            'pageNext' : pageNext,
                                            'pageFirst': pageFirst,
                                            'pageSecond' : pageSecond,
                                            'pageThird' : pageThird
                                        })

@login_required(login_url='login')
def showNewManager(request):
    if request.method == 'POST':

        name = request.POST.get("name")
        email = request.POST.get("email")
        cellphone = request.POST.get("cellphone")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        isSuperAdmin = request.POST.get("isSuperAdmin")
        isStaff = True

        email_exists = manager.objects.filter(email=email).exists()

        if email_exists:
            error_message = "Este correo ya esta en uso. Elija otro."
            return render(request, 'newManager.html', {
                                                        'error_message': error_message, 
                                                        'name':name, 
                                                        'email':email, 
                                                        'cellphone':cellphone, 
                                                        'password':password, 
                                                        'password_confirmation':password_confirmation,
                                                        })

        if password != password_confirmation:
            error_message = "Las contraseñas no coinciden. Intentelo de nuevo."
            return render(request, 'newManager.html', {
                                                        'error_message': error_message, 
                                                        'name':name, 
                                                        'email':email, 
                                                        'cellphone':cellphone, 
                                                        'password':password, 
                                                        'password_confirmation':password_confirmation,
                                                        })
        


        if isSuperAdmin == 'true':
            boolValueAdmin = True
        else:
            boolValueAdmin = False


        manager.objects.create(name=name, email=email, cellphone=cellphone, password= make_password(password), is_superuser=boolValueAdmin, is_staff= isStaff)
        return redirect('/SEL4C/managerTable/1/')

        # form = managerForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect('/SEL4C/managerTable/1/')
    else:
        form = managerForm()

    return render(request, 'newManager.html', {'form': form})

@login_required(login_url='login')
def deleteManager(request, id):
    managerN = manager.objects.get(pk=id)
    managerN.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect('/SEL4C/managerTable/1/')

# USUARIOS

@login_required(login_url='login')
def showUsers(request, page):
    start  = ((page-1)*100)
    end  = 99 + ((page-1)*100)
    data = user.objects.all()[start:end]  # Retrieve data from your database using your model
    
    if(page == 1):
        pagePrev = 1
        pageCurr = 1
        pageNext = 2
        pageFirst = 1
        pageSecond = 2
        pageThird = 3
    else:
        pagePrev = page-1
        pageCurr = page
        pageNext = page+1
        pageFirst = pagePrev
        pageSecond = pageCurr
        pageThird = pageNext



    return render(request, 'users.html', {
                                            'data': data, 
                                            'pagePrev':pagePrev,
                                            'pageNext' : pageNext,
                                            'pageFirst': pageFirst,
                                            'pageSecond' : pageSecond,
                                            'pageThird' : pageThird
                                        })

@login_required(login_url='login')
def deleteUser(request, id):
    userN = user.objects.get(pk=id)
    userN.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect('/SEL4C/usersTable/1/')

@login_required(login_url='login')
@csrf_exempt
def updateUser(request):
    response_data = {"message": "failure"}
    
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            userIDJSON = data['userID']
            nameJSON = data['name']
            emailJSON = data['email']
            passwordJSON = data['password']


            activeUser = user.objects.get(pk=userIDJSON)

            activeUser.name = nameJSON
            activeUser.email = emailJSON
            activeUser.password = passwordJSON
            activeUser.save()
        except:
            return JsonResponse(response_data)

        

        response_data = {
                            "successful": True,
                        }
        
    return JsonResponse(response_data)

# RENDER ACTIVIDADES 
@login_required(login_url='login')
def showActivities(request, id):
    activeUser = user.objects.get(pk=id)
    actDone = []
    if activeUser.actInit:
        actDone.append(True)
    else:
        actDone.append(False)

    if activeUser.act1ID:
        actDone.append(True)
    else:
        actDone.append(False)

    if activeUser.act2ID:
        actDone.append(True)
    else:
        actDone.append(False)

    if activeUser.act3ID:
        actDone.append(True)
    else:
        actDone.append(False)

    if activeUser.act4ID:
        actDone.append(True)
    else:
        actDone.append(False)

    if activeUser.actFinal:
        actDone.append(True)
    else:
        actDone.append(False)
    context = {
        'unlockable': json.dumps(actDone),
        'myId': id
    }

    return render(request, 'activities.html', context)

@login_required(login_url='login')
def showInitialDiagnosis(request, id):
    activeUser = user.objects.get(pk=id)
    object = actInicial.objects.get(pk= activeUser.actInit.pk)
    split = object.listOfAnswers.split()
    transformed_array = [(int(item)-1) * 25 for item in split]
    transformed_array = [5 if x == 0 else x for x in transformed_array]
    context = {
        'answers': transformed_array,
        'user': activeUser
    }
    return render(request, 'activities/initialDiagnosis.html', context)

@login_required(login_url='login')
def showActivity1(request, id):
    activeUser = user.objects.get(pk=id)
    object = act1.objects.get(pk= activeUser.act1ID.pk)
    context = {
        'all': object,
        'user': activeUser
    }
    return render(request, 'activities/activity1.html', context)

@login_required(login_url='login')
def showActivity2(request, id):
    activeUser = user.objects.get(pk=id)
    object = act2.objects.get(pk= activeUser.act2ID.pk)
    context = {
        'all': object,
        'user': activeUser
    }
    return render(request, 'activities/activity2.html', context)

@login_required(login_url='login')
def showActivity3(request, id):
    activeUser = user.objects.get(pk=id)
    object = act3.objects.get(pk= activeUser.act3ID.pk)
    context = {
        'reflection_text': object.reflection,
        'user': activeUser
    }
    return render(request, 'activities/activity3.html', context)

@login_required(login_url='login')
def showActivity4(request, id):
    activeUser = user.objects.get(pk=id)
    video = act4.objects.get(pk= activeUser.act4ID.pk)
    context = {
        'video_url': video.link,
        'user': activeUser
    }
    return render(request, 'activities/activity4.html', context)

@login_required(login_url='login')
def showFinalDeliverable(request, id):
    activeUser = user.objects.get(pk=id)
    video = actFinal.objects.get(pk= activeUser.actFinal.pk)
    context = {
        'video_url': video.link,
        'user': activeUser
    }
    return render(request, 'activities/finalDeliverable.html', context)

# CUENTA

@login_required(login_url='login')
def showAccount(request):
    if request.method == 'POST':

        name = request.POST.get("name")
        email = request.POST.get("email")
        cellphone = request.POST.get("cellphone")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        password_current = request.POST.get("password_current")

        if password != password_confirmation:
            error_message = "Las contraseñas no coinciden. Intentelo de nuevo."
            return render(request, 'account.html', {
                                                        'error_message': error_message, 
                                                        'user_name':name, 
                                                        'user_email':email, 
                                                        'user_cellphone':cellphone
                                                        })
        
        
        current = manager.objects.get(email=request.user)

        if(not check_password(password_current,current.password)):
            error_message = "Las contraseña actual es incorrecta. Intentelo de nuevo."
            return render(request, 'account.html', {
                                                        'error_message': error_message, 
                                                        'user_name':name,
                                                        'user_email':email, 
                                                        'user_cellphone':cellphone
                                                        })
        

        # Update the user's information
        current.name = name
        current.email = email
        current.cellphone = cellphone
        if password != "":
            current.password = make_password(password)
        current.save()

        return redirect('account')


    user_name = request.user.name
    user_email = request.user.email
    user_cellphone = request.user.cellphone
    context = {
        'user_name':user_name,
        'user_email':user_email,
        'user_cellphone':user_cellphone
    }
    return render(request, 'account.html', context)

@login_required(login_url='login')
@csrf_exempt
def loginUser(request):
    response_data = {"message": "failure"}
    if request.method == 'POST':
        data = json.loads(request.body)


        try:
            emailJSON = data['email']
            passwordJSON = data['password']

            items = user.objects.filter(email=emailJSON)
            if items.exists():
                for item in items:
                    if item.password == passwordJSON:
                        response_data = {
                                            "successful": True,
                                            "userID": item.id
                                        }
                else:
                    return JsonResponse(response_data)            
        except:
            return JsonResponse(response_data)

    return JsonResponse(response_data)

# GET REQUEST
@login_required(login_url='login')
def accountUser(request):
    response_data = {"message": "failure"}

    data = json.loads(request.body)

    try:
        userIDJSON = data['userID']

        activeUser = user.objects.get(pk=userIDJSON)

    except:
        return JsonResponse(response_data)

    response_data = {
                        "name" : activeUser.name,
                        "email" : activeUser.email,
                        "password" : activeUser.password,
                    }

    return JsonResponse(response_data)

@login_required(login_url='login')
def getDI(request):
    response_data = {"message": "failure"}

    data = json.loads(request.body)

    try:
        userIDJSON = data['userID']

        activeUser = user.objects.get(pk=userIDJSON)
        activity = actInicial.objects.get(pk=activeUser.actInit.pk)

        questionsJSON = [int(x) for x in activity.listOfAnswers.split()]
        

    except:
        return JsonResponse(response_data)

    response_data = {
                        "questions" : questionsJSON
                    }

    return JsonResponse(response_data)

@login_required(login_url='login')
def getAct1(request):
    response_data = {"message": "failure"}

    data = json.loads(request.body)
    try:
        userIDJSON = data['userID']

        activeUser = user.objects.get(pk=userIDJSON)
        activity = act1.objects.get(pk=activeUser.act1ID.pk)
        
        ideasJSON = [activity.ideas1, activity.ideas2, activity.ideas3, activity.ideas4, activity.ideas5]

    except:
        return JsonResponse(response_data)

    response_data = {
                        "ideas" : ideasJSON,
                        "interview" : activity.interview,
                    }

    return JsonResponse(response_data)

@login_required(login_url='login')
def getAct2(request):
    response_data = {"message": "failure"}

    data = json.loads(request.body)

    try:
        userIDJSON = data['userID']

        activeUser = user.objects.get(pk=userIDJSON)
        activity = act2.objects.get(pk=activeUser.act2ID.pk)
        
        ODSideasJSON = [activity.ODSideas1, activity.ODSideas2, activity.ODSideas3, activity.ODSideas4, activity.ODSideas5]
        consequencesJSON = [activity.consequences1, activity.consequences2, activity.consequences3, activity.consequences4, activity.consequences5]
        causesJSON = [activity.causes1, activity.causes2, activity.causes3]

    except:
        return JsonResponse(response_data)

    response_data = {
                        "ODSideas" : ODSideasJSON,
                        "consequences" : consequencesJSON,
                        "problem" : activity.problem,
                        "causes" : causesJSON
                    }

    return JsonResponse(response_data)

@login_required(login_url='login')
def getAct3(request):
    response_data = {"message": "failure"}

    data = json.loads(request.body)

    try:
        userIDJSON = data['userID']

        activeUser = user.objects.get(pk=userIDJSON)
        activity = act3.objects.get(pk=activeUser.act3ID.pk)
        

    except:
        return JsonResponse(response_data)

    response_data = {
                        "reflection" : activity.reflection
                    }

    return JsonResponse(response_data)

@login_required(login_url='login')
def getAct4(request):
    response_data = {"message": "failure"}

    data = json.loads(request.body)

    try:
        userIDJSON = data['userID']

        activeUser = user.objects.get(pk=userIDJSON)
        activity = act4.objects.get(pk=activeUser.act4ID.pk)
        

    except:
        return JsonResponse(response_data)

    response_data = {
                        "retro" : activity.link
                    }

    return JsonResponse(response_data)

@login_required(login_url='login')
def getEF(request):
    response_data = {"message": "failure"}

    data = json.loads(request.body)

    try:
        userIDJSON = data['userID']

        activeUser = user.objects.get(pk=userIDJSON)
        activity = actFinal.objects.get(pk=activeUser.actFinal.pk)
        

    except:
        return JsonResponse(response_data)

    response_data = {
                        "pitch" : activity.link
                    }

    return JsonResponse(response_data)

def currentAct(request):
    response_data = {"message": "failure"}

    data = json.loads(request.body)

    try:
        userIDJSON = data['userID']

        activeUser = user.objects.get(pk=userIDJSON)

    except:
        return JsonResponse(response_data)

    response_data = {
                        "successful": True,
                        "currentActivity": activeUser.currentActivity
                    }
    return JsonResponse(response_data)

# POST REQUEST

@csrf_exempt
def registerUser(request):
    response_data = {"message": "failure"}
    
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            nameJSON = data['name']
            genderJSON = data['gender']
            disciplineJSON = data['discipline']
            ageJSON = data['age']
            emailJSON = data['email']
            institutionJSON = data['institution']
            academicJSON = data['academic']
            countryJSON = data['country']
            passwordJSON = data['password']

            items = user.objects.filter(email=emailJSON)

            if items.exists():
                response_data = {
                                    "successful": False,
                                    "message": "Email already registered"    
                                }
                return JsonResponse(response_data)


            new_entry = user(name = nameJSON, age = ageJSON, country = countryJSON, 
                         institution = institutionJSON, password = passwordJSON, academic = academicJSON,
                         gender = genderJSON, discipline = disciplineJSON, email = emailJSON)
            new_entry.save()

        except:
            return JsonResponse(response_data)

        

        response_data = {"successful": True}
    return JsonResponse(response_data)

@csrf_exempt
def uploadDI(request):
    response_data = {"message": "failure"}
    
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            userIDJSON = data['userID']
            questionsJSON = data['questions']

            for element in questionsJSON:
                if not isinstance(element, int) or element < 1 or element > 5:
                    return JsonResponse(response_data)

            listOfAnswersJSON = ' '.join(map(str, questionsJSON))

            new_entry = actInicial(listOfAnswers = listOfAnswersJSON)
            new_entry.save()

            new_entry_id = new_entry.id


            activeUser = user.objects.get(pk=userIDJSON)
            newAct = actInicial.objects.get(pk=new_entry_id)

            activeUser.actInit = newAct
            activeUser.currentActivity = 1
            activeUser.progress = 16
            activeUser.save()
        except:
            return JsonResponse(response_data)

        

        response_data = {
                            "successful": True,
                            "currentActivity": 1
                        }
    return JsonResponse(response_data)

@csrf_exempt
def uploadAct1(request):
    response_data = {"message": "failure"}
    
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            userIDJSON = data['userID']
            ideasJSON = data['ideas']
            interviewJSON = data['interview']

            new_entry = act1(
                                ideas1 = ideasJSON[0], 
                                ideas2 = ideasJSON[1], 
                                ideas3 = ideasJSON[2], 
                                ideas4 = ideasJSON[3], 
                                ideas5 = ideasJSON[4], 
                                interview = interviewJSON
                            )
            new_entry.save()

            new_entry_id = new_entry.id


            activeUser = user.objects.get(pk=userIDJSON)
            newAct = act1.objects.get(pk=new_entry_id)

            activeUser.act1ID = newAct
            activeUser.currentActivity = 2
            activeUser.progress = 32
            activeUser.save()


            # evidenceJSON = data['evidence']
        except:
            return JsonResponse(response_data)

        response_data = {
                            "successful": True,
                            "currentActivity": 2
                        }
    return JsonResponse(response_data)

@csrf_exempt
def uploadAct2(request):
    response_data = {"message": "failure"}
    
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            userIDJSON = data['userID']
            ODSideasJSON = data['ODSideas']
            consequencesJSON = data['consequences']
            problemJSON = data['problem']
            causesJSON = data['causes']

            new_entry = act2(
                            ODSideas1 = ODSideasJSON[0],
                            ODSideas2 = ODSideasJSON[1],
                            ODSideas3 = ODSideasJSON[2],
                            ODSideas4 = ODSideasJSON[3],
                            ODSideas5 = ODSideasJSON[4],
                            consequences1 = consequencesJSON[0],
                            consequences2 = consequencesJSON[1],
                            consequences3 = consequencesJSON[2],
                            consequences4 = consequencesJSON[3],
                            consequences5 = consequencesJSON[4],
                            problem = problemJSON,
                            causes1 = causesJSON[0],
                            causes2 = causesJSON[1],
                            causes3 = causesJSON[2]
                            )
            new_entry.save()
            new_entry_id = new_entry.id


            activeUser = user.objects.get(pk=userIDJSON)
            newAct = act2.objects.get(pk=new_entry_id)

            activeUser.act2ID = newAct
            activeUser.currentActivity = 3
            activeUser.progress = 48
            activeUser.save()

        except:
            return JsonResponse(response_data)

        response_data = {
                            "successful": True,
                            "currentActivity": 3
                        }
    return JsonResponse(response_data)

@csrf_exempt
def uploadAct3(request):
    response_data = {"message": "failure"}
    
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            userIDJSON = data['userID']
            reflectionJSON = data['reflection']

            new_entry = act3(
                            reflection = reflectionJSON
                            )
            new_entry.save()
            new_entry_id = new_entry.id


            activeUser = user.objects.get(pk=userIDJSON)
            newAct = act3.objects.get(pk=new_entry_id)

            activeUser.act3ID = newAct
            activeUser.currentActivity = 4
            activeUser.progress = 64
            activeUser.save()

        except:
            return JsonResponse(response_data)

        response_data = {
                            "successful": True,
                            "currentActivity": 4
                        }
    return JsonResponse(response_data)

@csrf_exempt
def uploadAct4(request):
    response_data = {"message": "failure"}
    
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            userIDJSON = data['userID']
            retroJSON = data['retro']

            pattern = r"(https?://)?(www\.)?youtube\.com/watch\?v=([^&]+)"
            match = re.match(pattern, retroJSON)

            if not match:
                return JsonResponse(response_data)
 

            new_entry = act4(
                            link = retroJSON
                            )
            new_entry.save()
            new_entry_id = new_entry.id


            activeUser = user.objects.get(pk=userIDJSON)
            newAct = act4.objects.get(pk=new_entry_id)

            activeUser.act4ID = newAct
            activeUser.currentActivity = 5
            activeUser.progress = 80
            activeUser.save()

        except:
            return JsonResponse(response_data)

        response_data = {
                            "successful": True,
                            "currentActivity": 5
                        }
    return JsonResponse(response_data)

@csrf_exempt
def uploadEF(request):
    response_data = {"message": "failure"}
    
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            userIDJSON = data['userID']
            pitchJSON = data['pitch']

            pattern = r"(https?://)?(www\.)?youtube\.com/watch\?v=([^&]+)"
            match = re.match(pattern, pitchJSON)

            if not match:
                return JsonResponse(response_data)

            new_entry = actFinal(
                            link = pitchJSON
                            )
            new_entry.save()
            new_entry_id = new_entry.id


            activeUser = user.objects.get(pk=userIDJSON)
            newAct = actFinal.objects.get(pk=new_entry_id)

            activeUser.actFinal = newAct
            activeUser.currentActivity = 6
            activeUser.progress = 100

            activeUser.save()

        except:
            return JsonResponse(response_data)

        response_data = {
                            "successful": True,
                            "currentActivity": 6
                        }
    return JsonResponse(response_data)

# Viewsets

class userViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = userSerializer

class managerViewSet(viewsets.ModelViewSet):
    queryset = manager.objects.all()
    serializer_class = managerSerializer