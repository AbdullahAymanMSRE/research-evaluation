from django.contrib import admin
from .models import Faculty, Department, Team, Subject, Section

# Register your models here.

admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Section)
admin.site.register(Team)
admin.site.register(Subject)

