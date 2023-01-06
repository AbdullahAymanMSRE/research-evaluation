from django.urls import path
from .views import (
        main, 
        create_topic, 
        select_topic, 
        upload_research, 
        correcting,
        students_resaults,
    )

app_name="researches"

urlpatterns = [
    path('', main, name="main"),
    path('<int:id>/doctor/topics/', create_topic, name="create_topic"),
    path('<int:id>/topics/select/', select_topic, name="select_topic_to_correct"),
    path('<int:sid>/<int:rid>/upload/', upload_research, name="upload_research"),
    path('<int:sid>/<int:rid>/correcting/', correcting, name="correcting"),
    path('students_resaults/', students_resaults, name="students_resaults"),
]