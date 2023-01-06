from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model, authenticate, decorators
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# from ipware import get_client_ip


from .models import User

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('researches:main')
    return render(request, 'users/index.html', {})

def loginView(request, prof):  
    if request.user.is_authenticated:
        return redirect('researches:main')
  
    doctor = True if prof == "professor" else (False if prof == "student" else None)

    context = {'wrong': False}
    if prof  !=  None:
        context['prof'] = prof
        # FORM
        if request.method == "POST":
            users = User.objects.filter(doctor=doctor)
            try:
                user = users.get(national_id=request.POST['national_id'])
            except:
                context['wrong'] = True
                return render(request, 'users/login.html', context)


            request.session['ni'] = user.national_id
            if not user.email: return redirect('users:create_passwd', prof=prof)
            else: return redirect('users:passwd_login', prof=prof)

            if(user.doctor):
                return redirect('administration:choose')
            
            return redirect('researches:main')


        return render(request, 'users/login.html', context)

    else:
        return redirect("users:home")

def passwd_login(request, prof):
    if request.user.is_authenticated:
        return redirect('researches:main')
  
    if not 'ni' in request.session:
        return redirect('users:home')

    doctor = True if prof == "professor" else (False if prof == "student" else None)
    ni = request.session['ni']

    users = User.objects.filter(doctor=doctor)
    user = users.get(national_id=ni)

    if not user.email:
        return redirect('users:passwd_login', prof=prof)

    context = {'wrong': False, 'ni': ni, "email": user.email}
    if prof  !=  None:
        context['prof'] = prof
        if request.method == 'POST':
            
            authed_user = authenticate(national_id=ni, password=request.POST['password'], name=user.name, doctor=doctor)
            if authed_user == None:
                context['wrong'] = True
                return render(request, 'users/passwd_login.html', context)

            login(request, user=authed_user)
#            ip, is_routable = get_client_ip(request)
#            send_mail('كلمة السر منصة الموضوعات البحثية',
#                    ip,
#                    settings.EMAIL_HOST_USER,
#                    ['abdallaamsre@gmail.com'], 
#                    fail_silently=True)
#
            return redirect('administration:choose')
            
                
        return render(request, 'users/passwd_login.html', context)
    else:
        return redirect("users:home")

def create_passwd(request, prof):
    if request.user.is_authenticated:
        return redirect('researches:main')

    if not 'ni' in request.session:
        return redirect('users:home')

    doctor = True if prof == "professor" else (False if prof == "student" else None)
    ni = request.session['ni']

    users = User.objects.filter(doctor=doctor)
    user = users.get(national_id=ni)

    if user.email:
        return redirect('users:passwd_login', prof=prof)


    context = {'wrong': False}
    if prof  !=  None:
        context['prof'] = prof

        if request.method == 'POST':
            user.email = request.POST['email']
            try:
                user.save()
            except:
                context['wrong'] = True
                return render(request, 'users/create_passwd.html', context)

            _pass = User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYabcdefghjkmnpqrstuvwxyz23456789')
            user.set_password(_pass)
            user.save()

            send_mail('كلمة السر منصة الموضوعات البحثية',
                    f"""
                        كلمة السر الخاصة بك هي : 
                        {_pass}
                        الاسم : {user.name}
                        الرقم القومي : {user.national_id}
                    """,
                    settings.EMAIL_HOST_USER,
                    [request.POST['email']], 
                    fail_silently=True)

            return redirect('users:passwd_login', prof=prof)

        return render(request, 'users/create_passwd.html', context)
    
    else:
        return redirect("users:home")

@decorators.login_required
def logout_view(request):
    logout(request)
    return redirect("users:home")


