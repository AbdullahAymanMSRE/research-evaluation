from django.urls import path
from .views import home, loginView, logout_view, create_passwd, passwd_login

app_name="users"

urlpatterns = [
    path('', home, name="home"),
    path('<str:prof>/login/', loginView, name="login"),
    path('<str:prof>/create_password/', create_passwd, name="create_passwd"),
    path('<str:prof>/password_login/', passwd_login, name="passwd_login"),

    path('logout/', logout_view, name="logout")
]