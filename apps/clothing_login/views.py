from django.shortcuts import render, redirect, HttpResponse
from apps.clothing_dojo.models import *
from djangounchained_flash import ErrorManager, getFromSession

def index(request):
    if 'flash' not in request.session:
        request.session['flash']=ErrorManager().addToSession()
    if 'userID' in request.session:
        return redirect('/')
    if 'remember' not in request.session:
        request.session['remember']=''
    if 'login_email' not in request.session:
        request.session['login_email']=''
    e=getFromSession(request.session['flash'])
    context={
        'login_main_errors':e.getMessages('login_main'),
        'login_email_errors':e.getMessages('login_email'),
        'reg_good':e.getMessages('reg_good'),
        'checked':request.session['remember'],
        'login_email':request.session['login_email']
    }
    request.session['flash']=e.addToSession()
    return render(request,'clothing_login/login.html', context)

def processLogin(request):
    if request.method!='POST':
        print('Hacker alert')
        return redirect('/')
    errors=User.objects.validate_login(request.POST)
    e=getFromSession(request.session['flash'])
    if len(errors):
        for tag,error in errors.items():
            e.addMessage(error,tag)
        request.session['flash']=e.addToSession()
        return redirect('/login/')
    if 'remember_me' in request.POST:
        print('Remembering user')
        request.session['login_email']=request.POST['email']
        request.session['remember']='checked'
    else:
        request.session['login_email']=''
        request.session['remember']=''
    this_user=User.objects.get(email=request.POST['email'])
    request.session['flash']=e.addToSession()
    request.session['loggedIn']=True
    request.session['userID']=this_user.id
    return redirect('/')

def register(request):
    if 'flash' not in request.session:
        request.session['flash']=ErrorManager().addToSession()
    if 'userID' in request.session:
        return redirect('/')
    if 'remember' not in request.session:
        request.session['remember']=''
    if 'login_email' not in request.session:
        request.session['login_email']=''
    if 'first_name' not in request.session:
        request.session['first_name']=''
        request.session['last_name']=''
        request.session['email']=''
        request.session['location']=''
    e=getFromSession(request.session['flash'])
    # msgs=e.getMessages()
    # print(msgs)
    context={
        'locations':Location.objects.all(),
        'first_name':request.session['first_name'],
        'last_name':request.session['last_name'],
        'email':request.session['email'],
        'location':request.session['location'],
        'first_name_errors':e.getMessages('first_name'),
        'last_name_errors':e.getMessages('last_name'),
        'reg_email_errors':e.getMessages('reg_email'),
        'password_errors':e.getMessages('password'),
        'confirm_errors':e.getMessages('confirm')
    }
    request.session['flash']=e.addToSession()
    return render(request, 'clothing_login/register.html', context)

def processRegister(request):
    if request.method!='POST':
        print('Hack attempted')
        return redirect('/login/')
    print('Processing register')
    errors=User.objects.validate_register(request.POST)
    e=getFromSession(request.session['flash'])
    if len(errors):
        request.session['first_name']=request.POST['first_name']
        request.session['last_name']=request.POST['last_name']
        request.session['email']=request.POST['email']
        request.session['location']=request.POST['location']
        for tag,error in errors.items():
            e.addMessage(error, tag)
        request.session['flash']=e.addToSession()
        return redirect('/login/register/')
    location=Location.objects.get(name=request.POST['location'])
    cohort_toAdd=Cohort.objects.get(location=location)
    User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()), cohort=cohort_toAdd)
    request.session['first_name']=''
    request.session['last_name']=''
    request.session['email']=''
    request.session['location']=''
    e.addMessage('Registration successful!', 'reg_good')
    request.session['flash']=e.addToSession()
    return redirect('/login')