from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import *
# Create your views here.

@login_required
@user_passes_test(
    lambda u: u.doctor,
    redirect_field_name="researches:main"
)
def adding_subjects(request):
    member = request.user
    faculties = []
    for f in Faculty.objects.all():
        faculties.append(f)
    if request.method == "POST":
        member.subjects.clear()
        count = 0
        while count < int(request.POST['lenEntries']):
            faculty = Faculty.objects.filter(name=request.POST[f'faculty{count+1}']).first()
            team = Team.objects.get(name=request.POST[f'team{count+1}'], faculty=faculty)
            section = Section.objects.get(name=request.POST[f'section{count+1}'], department__faculty=faculty)
            subject = Subject.objects.get(name=request.POST[f'subject{count+1}'], team=team, section=section)
            
            member.subjects.add(subject)

            count += 1

        return redirect('researches:main')


    context = {
        "member": member,
        "faculties": faculties}
    return render(request, 'unistruct/adding_subjects.html', context)
