from django.urls import path,re_path
from .views import *

app_name="domain"
urlpatterns = [
    path('login/',Login.as_view(),name='login'),
    path('parentlogin/',ParentLogin.as_view(),name='parentlogin'),
    path('parentdata/',ParentData.as_view(),name='parentdata'),
    path('index/',Index.as_view(),name='index'),
    path('indexdata/',IndexData.as_view(),name='indexdata'),
    path('mainindex/',MainIndex.as_view(),name='mainindex'),
    path('mainindexdata/',MainIndexData.as_view(),name='mainindexdata'),
    path('jumpindex/',JumpIndex.as_view(),name='jumpindex'),
    path('jumpindexdata/',JumpIndexData.as_view(),name='jumpindexdata'),
    path('createjump/',CreateJump.as_view(),name='createjump'),
    path('createmain/',CreateMain.as_view(),name='createmain'),
    path('editmain/',EditMain.as_view(),name='editmain'),
    path('createindex/',CreateIndex.as_view(),name='createindex'),
    path('logout/',Logout.as_view(),name='logout'),
]

