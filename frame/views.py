from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from frame.forms import LoginForm, RegisterForm
from frame.models import Task
from django.contrib.auth import authenticate, login
from django.core import serializers
import simplejson


def index(request):
    login = LoginForm(request.POST or None)
    register = RegisterForm(request.POST or None)
    return direct_to_template(request, 'index.html', { 'login': login, 'register': register })
    
def tasks(request):
    if request.user.is_authenticated():
        tasks = Task.objects.filter(user=request.user)
        success = True
        message = "Ok"
        data = serializers.serialize('json', tasks)
        payload = {'success': success, 'message': message, 'data': data }
        return HttpResponse(simplejson.dumps(payload), content_type='application/json')        
    success = False
    message = "You don't have auth."
    payload = {'success': success, 'message': message }
    return HttpResponse(simplejson.dumps(payload), content_type='application/json')
    
def add_task(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            task = Task(title=request.GET['task'], user=request.user)
            task.save()
            success = True
            message = "Ok"
            data = task.id
            payload = {'success': success, 'message': message, 'data': data }
            return HttpResponse(simplejson.dumps(payload), content_type='application/json')        
    success = False
    message = "Something wrong with task."
    payload = {'success': success, 'message': message }
    return HttpResponse(simplejson.dumps(payload), content_type='application/json')        
    
def del_task(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            try:
                task = Task.objects.get(pk=request.GET['id']).delete()
            except: 
                success = False
                message = "Doesn't exist"
                payload = {'success': success, 'message': message }
                return HttpResponse(simplejson.dumps(payload), content_type='application/json')        
            success = True
            message = "Removed"
            payload = {'success': success, 'message': message }
            return HttpResponse(simplejson.dumps(payload), content_type='application/json')        
    success = False
    message = "Something wrong with removing this task."
    payload = {'success': success, 'message': message }
    return HttpResponse(simplejson.dumps(payload), content_type='application/json')       
            
def update_task(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            task = Task.objects.get(pk=request.GET['id'])
            task.title=request.GET['title']
            task.save()
            success = True
            message = "Updated"
            payload = {'success': success, 'message': message }
            return HttpResponse(simplejson.dumps(payload), content_type='application/json')
    success = False
    message = "Something wrong with updating this task."
    payload = {'success': success, 'message': message }
    return HttpResponse(simplejson.dumps(payload), content_type='application/json')
    
def user_info(request):
    if request.user.is_authenticated():
        return direct_to_template(request, 'user_info.html', { 'user': request.user })
    else:
        return HttpResponseForbidden()
    
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            success = True
            message = "Ok!"
            payload = {'success': success, 'message': message }
            return HttpResponse(simplejson.dumps(payload), content_type='application/json')        
    success = False
    message = "Your username and password were incorrect."
    payload = {'success': success, 'message': message }
    return HttpResponse(simplejson.dumps(payload), content_type='application/json')        
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()  
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            success = True
            message = "Registration done."
            payload = {'success': success, 'message': message }
            return HttpResponse(simplejson.dumps(payload), content_type='application/json')
    else:
        form = RegisterForm()
    data = errors_to_json(form.errors)   
    success = False
    message = "Validation failed."
    payload = {'success': success, 'message': message, 'data':data}
    return HttpResponse(simplejson.dumps(payload),
                    content_type='application/json',
                )    
    
def errors_to_json(errors):
    """
    Convert a Form error list to JSON::
    """
    return dict(
            (k, map(unicode, v))
            for (k,v) in errors.iteritems()
        )
    