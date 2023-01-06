from django.urls import path

from .views import adding_subjects

app_name = "unistruct"

urlpatterns = [
    path('', adding_subjects, name="adding_subjects")
]