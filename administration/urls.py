from django.urls import path

from .views import (
        choose, upload_data, 
        resaults, 
        privileges, 
        approval, 
        subjects_report, 
        reports,
        download_compressed_folder
    )

app_name = "administration"

urlpatterns = [
    path('', choose, name="choose"),
    path('upload/', upload_data, name="upload_data"),
    path('results/', resaults, name="resaults"),
    path('privileges/', privileges, name="privileges"),
    path('approval/', approval, name="approval"),
    path('subjects/data/', subjects_report, name="subjects_report"),
    path('subjects/reports/', reports, name="reports"),
    path('results/download-compressed-folder/', download_compressed_folder, name="download_compressed_folder")
]

