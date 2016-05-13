from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password
from django.core import serializers
from django.core.exceptions import ValidationError as DjangoValidationError 
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import dateparse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie 
import bleach
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonValidationError
from . import models, decorators

@ensure_csrf_cookie
def index(request):
    return render(request, 'ausome_sports/index.html')

@decorators.login_required
def get_user_profile(request):
    profile_set = models.AusomeUser.objects.filter(user=request.user)
    data = serializers.serialize('json', profile_set)

    return HttpResponse(data, content_type='application/json')

@require_POST
def post_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            data = {'msg': 'Success!'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data = {'msg': 'Account disabled'}
            denied = HttpResponse(json.dumps(data), content_type='application/json')
            denied.status_code = 401
            return denied 
    else:
        data = {'msg': 'Username and/or password incorrect'}
        denied = HttpResponse(json.dumps(data), content_type='application/json')
        denied.status_code = 401
        return denied 

@require_POST
def post_create_user(request):
    # check for existing username

    # Validate POST contents
    try:
        validate(request.POST, schema.new_account)
    except JsonValidationError as error:
        error_msg = error.schema.get('error_msg')
        data = {'msg': error_msg if error_msg not None else error.message}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    username = bleach.clean(request.POST.get('username'))
    
    password = request.POST.get('password')
    # validate password
    try:
        validate_password(password)
    except DjangoValidationError as error:
        data = {'msg': error.message}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    email = bleach.clean(request.POST.get('email'))
    user = User.objects.create_user(username,
            email,
            password,
            )
    user.first_name = bleach.clean(request.POST.get('first_name'))
    user.last_name = bleach.clean(request.POST.get('last_name'))
    try:
        user.dob = dateparse.parse_date(request.POST.get('dob'))
    except ValueError as error:
        data = {'msg': error.message}
        invalid = HttpResponse(json.dumps(data), content_type='application/json')
        invalid.status_code = 400
        return invalid 

    user.sex = bleach.clean(request.POST.get('sex')).lower()
    user.phone = bleach.clean(request.POST.get('phone'))
    user.visible_in_directory = True if request.POST.get('visible_in_directory').lower() == 'y' else False 
    user.save()

    data = {'msg': 'Account created!'}
    return HttpResponse(json.dumps(data), content_type='application/json')
