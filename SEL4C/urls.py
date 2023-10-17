from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from SEL4C import views

router = routers.DefaultRouter()
router.register(r'users',views.userViewSet)
router.register(r'managers',views.managerViewSet)



urlpatterns = [
    path('login/', views.showLogin, name='login'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('admin/', include(router.urls)),
    path('index/', views.showIndex, name='index'),
    path('account/', views.showAccount, name='account'),

    # MANAGERS

    path('deleteManager/<int:id>/', views.deleteManager, name='manager_delete'),
    path('managerTable/<int:page>/', views.showManagers, name='managers'),
    path('managerTable/newManager/', views.showNewManager, name='newManager'),

    # USERS

    path('usersTable/<int:page>/', views.showUsers, name='users'),
    path('deleteUser/<int:id>/', views.deleteUser, name='user_delete'),

    # ACTIVIDADES

    path('userActivities/<int:id>/', views.showActivities, name='user_activities'),
    path('userActivities/<int:id>/initialDiagnosis/', views.showInitialDiagnosis, name='initial_diagnosis'),
    path('userActivities/<int:id>/userActivity1/', views.showActivity1, name='activity1'),
    path('userActivities/<int:id>/userActivity2/', views.showActivity2, name='activity2'),
    path('userActivities/<int:id>/userActivity3/', views.showActivity3, name='activity3'),
    path('userActivities/<int:id>/userActivity4/', views.showActivity4, name='activity4'),
    path('userActivities/<int:id>/finalDeliverable/', views.showFinalDeliverable, name='final_deliverable'),

    # GET REQUEST
    path('loginUser/', views.loginUser, name='loginUser'),
    path('currentAct/', views.currentAct, name='currentAct'),
    path('accountUser/', views.accountUser, name='accountUser'),
    path('getDI/', views.getDI, name='getDI'),
    path('getAct1/', views.getAct1, name='getAct1'),
    path('getAct2/', views.getAct2, name='getAct2'),
    path('getAct3/', views.getAct3, name='getAct3'),
    path('getAct4/', views.getAct4, name='getAct4'),
    path('getEF/', views.getEF, name='getEF'),


    # POST REQUEST
    path('registerUser/', views.registerUser, name='registerUser'),
    path('uploadDI/', views.uploadDI, name='uploadDI'),
    path('uploadAct1/', views.uploadAct1, name='uploadAct1'),
    path('uploadAct2/', views.uploadAct2, name='uploadAct2'),
    path('uploadAct3/', views.uploadAct3, name='uploadAct3'),
    path('uploadAct4/', views.uploadAct4, name='uploadAct4'),
    path('uploadEF/', views.uploadEF, name='uploadEF'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)