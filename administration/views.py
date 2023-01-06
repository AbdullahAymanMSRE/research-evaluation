
import xlrd
import os
import zipfile
import io


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
from django.http import HttpResponse

from unistruct.models import Faculty, Team, Department, Section, Subject
from users.models import User
from researches.models import Research, StudentResearch

# Create your views here.

@login_required
@user_passes_test(
    lambda u: u.doctor,
    redirect_field_name="researches:main"
)
def choose(request):
    return render(request, 'administration/choose.html', {})

@login_required
@user_passes_test(
    lambda u: u.staff,
    redirect_field_name="researches:main"
)
def upload_data(request):
    if request.method == "POST":
        files = request.FILES
        # SUBJECTS
        try:
            input_excel = files['subjects']

            wb = xlrd.open_workbook(file_contents = input_excel.read(), encoding_override = 'utf8')
            sheet = wb.sheet_by_index(0)
            for i in range(1, sheet.nrows-1):
                cv = sheet.row_values(i)
                facl = str(cv[4]).strip()
                sec = str(cv[3]).strip()
                dprt = str(cv[2]).strip()
                tem = str(cv[1]).strip()
                subj = str(cv[0]).strip()

                faculty, _ = Faculty.objects.get_or_create(name=facl)
                team, _ = Team.objects.get_or_create(name=tem, faculty=faculty)
                department, _ = Department.objects.get_or_create(name=dprt, faculty=faculty)
                section, _ = Section.objects.get_or_create(name=sec, department=department)
                subject, _ = Subject.objects.get_or_create(name=subj, section=section, team=team)

        except MultiValueDictKeyError:
            pass

        except:
            print('error')

        # MEMBERS
        try:
            input_excel = files['members']
            
            wb = xlrd.open_workbook(file_contents = input_excel.read(), encoding_override = 'utf8')
            sheet = wb.sheet_by_index(0)

            for i in range(1, sheet.nrows-1):
                cv = sheet.row_values(i)
                mfacl = str(cv[2]).strip()
                mdprt = str(cv[3]).strip()
                ni = str(int(float(str(cv[0]))))
                mbr = str(cv[1]).strip()


                mfaculty, _ = Faculty.objects.get_or_create(name=mfacl)
                mdepartment, _ = Department.objects.get_or_create(name=mdprt, faculty=mfaculty)
                try:
                    member, _ = User.objects.get_or_create(
                        national_id= ni,
                        name = mbr,
                        doctor = True,
                        faculty=mfaculty,
                        department= mdepartment,
                        password= "doc"
                    )
                except:
                    pass

        except MultiValueDictKeyError:
            pass

        except:
            print('error')
        



        # STUDENTS
        try:
            input_excel = files['students']

            wb = xlrd.open_workbook(file_contents = input_excel.read(), encoding_override = 'utf8')
            sheet = wb.sheet_by_index(0)

            for i in range(1, sheet.nrows):
                cv = sheet.row_values(i)

                ni = str(int(float(str(cv[0]))))
                mbr = str(cv[1]).strip()
                facl = str(cv[2]).strip()
                tem = str(cv[3]).strip()
                stem = str(cv[5]).strip()
                dprt = str(cv[6]).strip()
                sec = str(cv[7]).strip()
                subj = str(cv[8]).strip()
                email, emailpasswd = None, None
                if len(cv) == 11 :
                    email = str(cv[9]).strip() 
                    emailpasswd = str(cv[10]).strip() 
                
                faculty, _ = Faculty.objects.get_or_create(name=facl)
                team, _ = Team.objects.get_or_create(name=tem, faculty=faculty)
                steam, _ = Team.objects.get_or_create(name=stem, faculty=faculty)
                department, _ = Department.objects.get_or_create(name=dprt, faculty=faculty)
                section, _ = Section.objects.get_or_create(name=sec, department=department)
                subject, _ = Subject.objects.get_or_create(name=subj, section=section, team=steam)
                if len(User.objects.filter(national_id=ni)) == 1:
                    student = User.objects.get(national_id=ni) 
                    if email and emailpasswd:
                        student.official_email = email 
                        student.official_email_passwd = emailpasswd
                        student.save()
                    student.subjects.add(subject)
                else:
                    try:
                        student, _ = User.objects.get_or_create(
                            national_id= ni,
                            name = mbr,
                            doctor = False,
                            faculty=faculty,
                            team= team,
                            password= "stu"
                        )

                        student.subjects.add(subject)
                        if email and emailpasswd:
                            student.official_email = email
                            student.official_email_passwd = emailpasswd
                            student.save()
                    except:
                        pass

        except MultiValueDictKeyError:
            pass

        except:
            raise ValueError('Error')

    return render(request, 'administration/upload_data.html', {})

@login_required
@user_passes_test(
    lambda u: u.control_head,
    redirect_field_name="researches:main"
)
def resaults(request):
    context = {
        "students": User.objects.filter(doctor=False),
        "faculties": Faculty.objects.all()}
    return render(request, 'administration/resaults.html', context)

@login_required
@user_passes_test(
    lambda u: u.staff,
    redirect_field_name="researches:main"
)
def privileges(request):
    context = {}
    if request.user.admin:
        context['faculties'] = Faculty.objects.all()
    else:
        context['teams'] = request.user.faculty.teams.all()
    if request.method == "POST":
        post = list(dict(request.POST).items())[1:]

        if request.user.admin:
            for d in post:
                dean = User.objects.get(national_id=d[1][0])
                dean.staff=True
                dean.control_head = True
                dean.save()
        else:
            for ch in post:
                control_head = User.objects.get(national_id=ch[1][0])
                control_head.control_head=True
                control_head.team = Team.objects.get(id=int(ch[0]))
                control_head.save()

    return render(request, 'administration/privileges.html', context)

@login_required
@user_passes_test(
    lambda u: u.control_head,
    redirect_field_name="researches:main"
)
def approval(request):
    context = {'faculties': Faculty.objects.all()}
    if request.method == "POST":
        try:
            post = list(dict(request.POST).keys())[1:]
        except:
            post = []
        if request.user.staff:
            for team_id in post:
                team = Team.objects.get(id=int(team_id))
                team.done = True
                team.save() 
        else:
            for subject_id in post:
                subject = Subject.objects.get(id=int(subject_id))
                subject.done = True
                subject.save() 
    return render(request, 'administration/approval.html', context)


@login_required
@user_passes_test(
    lambda u: u.staff or u.dprtmngr,
    redirect_field_name="researches:main"
)
def subjects_report(request):
    member = request.user

    if member.admin:
        context = {
            'faculties': Faculty.objects.order_by('name'),
        }
    elif member.staff:
        context = {
            'entries':member.faculty.members_list,
            'departments': member.faculty.departments_list,
            'subjs_number': member.faculty.subjs_number,
        }
    else:
        context = {
            'entries': member.department.members_list,
            'departments': member.faculty.departments.filter(name=member.department),
            'subjs_number': member.department.subjs_number,
        }

    return render(request, 'administration/subjects_report.html', context)


@login_required
@user_passes_test(
    lambda u: u.control_head,
    redirect_field_name="researches:main"
)
def reports(request):
    context = {
        "subjects": Subject.objects.all(),
        "faculties": Faculty.objects.all()}
    return render(request, 'administration/reports.html', context)

@login_required
@user_passes_test(
    lambda u: u.control_head and not u.staff,
    redirect_field_name="researches:main"
)
def download_compressed_folder(request):
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_dir_name = f"student_researches"
    zip_filename = f"{zip_dir_name}.zip"

    # Open StringIO to grab in-memory ZIP contents
    s = io.BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for sr in StudentResearch.objects.filter(research__subject__in=request.user.team.subjects.all()):
        # Calculate path for file in zip
        zip_path = os.path.join(zip_dir_name, sr.research_file.name)

        # Add file, at correct path
        zf.write(os.path.join(settings.MEDIA_ROOT, sr.research_file.name), zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = f'attachment; filename={zip_filename}' 

    return resp

