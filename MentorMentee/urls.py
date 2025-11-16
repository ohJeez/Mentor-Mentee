from django.urls import path

from . import views

#URL's
#path('pathname',functionName)
urlpatterns=[
    path('',views.home,name='home')
]