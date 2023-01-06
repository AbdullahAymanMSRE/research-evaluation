import re
import json
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext

from users.models import User
from unistruct.models import Subject
from .models import Research, StudentResearch
# Create your views here.

@login_required
def main(request):
    if not request.user.doctor:
        if request.user.team.done:
            return redirect('researches:students_resaults')
    return render(request, 'researches/main.html', {})

@login_required
def create_topic(request, id):
    if not request.user.doctor:
        return redirect('researches:main')
    selected_subject = get_object_or_404(Subject, id=id)
    if not selected_subject in request.user.subjects.all():
        return redirect('researches:main')

    context = {'selected_subject': selected_subject}
    if request.method == "POST":
        Research.objects.filter(subject=selected_subject).delete()
        count = 0
        while count < int(request.POST['numr']):
            name = request.POST[f'subject-{count+1}']
            Research.objects.create(name=name, subject=selected_subject)

            count += 1

        return redirect('researches:main')
    return render(request, 'researches/create_topic.html', context)

@login_required
def select_topic(request, id):
    if not request.user.doctor:
        if request.user.team.done:
            return redirect('researches:students_resaults')

    selected_subject = get_object_or_404(Subject, id=id)
    if not selected_subject in request.user.subjects.all():
        return redirect('researches:main')
    context = {'selected_subject': selected_subject}
    if not request.user.doctor:
        selected_subject.rseen = True
        selected_subject.save()
        context['stu_h'] = False
        if request.user.student_researches.filter(research__subject=selected_subject):
            context['stu_h'] = request.user.student_researches.filter(research__subject=selected_subject).first()

    return render(request, 'researches/select_topic.html', context)


@login_required
def upload_research(request, sid, rid):
    # security
    if not request.user.doctor:
        if request.user.team.done:
            return redirect('researches:students_resaults')
    if request.user.doctor:
        return redirect('researches:main')

    # getting importatn information
    selected_subject = get_object_or_404(Subject, id=sid)

    if not selected_subject in request.user.subjects.all():
        return redirect('researches:main')

    selected_research = get_object_or_404(Research, id=rid)

    # initializing the context
    context = {'selected_subject': selected_subject,
               "open": (datetime.datetime.now() >= datetime.datetime(2020, 5,31) and datetime.datetime.now() < datetime.datetime(2020, 6,10))
    }
    # if the student has uploaded a research in this subject
    stu_h = request.user.student_researches.filter(research__subject=selected_subject)
    if stu_h:
        # if student trying to upload in other research
        if stu_h.first().research != selected_research:
            return redirect('researches:main')

        # sending student research with context
        context['stu_h'] = request.user.student_researches.filter(research__subject=selected_subject).first()

    # when the form in submitted
    if request.method == "POST":
        # loading colleagues data into dictionary called pst
        pst = json.loads(str(request.POST).replace('<QueryDict: ', '').replace(">",'').replace("'",'"'))

        # creating and setting file name
        fileName = f'{request.user.national_id[0:10]}'
        for colleague in pst.get('colleagues') if pst.get('colleagues') else []:
            colluser = User.objects.get(name=colleague)
            fileName+=f"-{colluser.national_id[0:10]}"
        request.FILES['file-7[]']._set_name(fileName)

        # delete any student research related to the student if exitsts and creating the new one
        request.user.student_researches.filter(research__subject=selected_subject).delete()
        stre = StudentResearch.objects.create(
            research_file=request.FILES['file-7[]'],
            research=selected_research)
        stre.students.add(request.user)

        # adding colleagues to student research
        for colleague in pst.get('colleagues') if pst.get('colleagues') else []:
            colluser = User.objects.get(name=colleague)
            stre.students.add(colluser)

        stre.save()
        return redirect('researches:upload_research', sid=selected_subject.id, rid=selected_research.id)

    # getting colleagues
    all_cols = request.user.team.students_list
    new_cols =[] 
    for col in all_cols:
        for sr in col.student_researches.all():
            if sr.research.subject == selected_subject:
                if sr == stu_h:
                    col.hasl = True
                    col.thisu = True
                else:
                    col.hasl = True
                    col.thisu = False
                break
            else:
                if sr == col.last_student_researches:
                    col.hasl = False
                    col.thisu = False

    context['cols'] = all_cols 
    context['selected_research']= selected_research = get_object_or_404(Research, id=rid)
    return render(request, 'researches/upload_research.html', context)

@login_required
def correcting(request, sid, rid):
    if not request.user.doctor:
        return redirect('researches:main')
    selected_subject = get_object_or_404(Subject, id=sid)
    if not selected_subject in request.user.subjects.all():
        return redirect('researches:main')
    selected_research = get_object_or_404(Research, id=rid)
    corrected_researches = StudentResearch.objects.filter(research=selected_research)
    for npr in corrected_researches.filter(seen=False):
        npr.seen = True
        npr.save()
    context = {
        'selected_subject': selected_subject,
        'selected_research': selected_research,
        'corrected_researches': corrected_researches,
    }
    if request.method == "POST":
        count = 1
        post = request.POST
        post_keys = list(request.POST.keys())
        while count < len(post_keys):
            item, num = post_keys[count].split('_')
            # i = -1
            # while (re.match(r'^-?\d+(?:\.\d+)?$', post_keys[count][i:]) is not None):
            #     num = post_keys[count][i:]
            #     i -= 1                  

            val = post[post_keys[count]]
            obj = corrected_researches.get(id=int(num))
            
            if item=="references": obj.references = int(val)
            elif item=="conclusions": obj.conclusions = int(val)
            elif item=="content": obj.content = int(val)
            elif item=="axes": obj.axes = int(val)
            elif item=="intro": obj.intro = int(val)
            else: raise ValueError('no input')
            
            obj.corrected = True
            obj.corrected_by = request.user

            obj.save()      

            count += 1

    return render(request, 'researches/correcting.html', context)

@login_required
@user_passes_test(
    lambda u: (not u.doctor) and (u.team.done),
    redirect_field_name="researches:main"
)
def students_resaults(request):
    return render(request, 'researches/students_resaults.html', {})

