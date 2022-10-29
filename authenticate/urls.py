from django.urls import path,include
from . import application
from . import views

urlpatterns = [
    path("signup",views.signup,name="signup"),
    path("",views.signin,name="signin"),
    path("index",views.index,name="index"),
    path("pred",application.predict,name="pred"),
    path("signout",views.signout,name="signout"),
]