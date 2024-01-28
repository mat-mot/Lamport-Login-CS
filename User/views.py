from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from User.forms import UserCreationForm, UserSigninForm
from User.models import User
from Utilities import hasher
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            hasher.set_password(user, form.cleaned_data['password'])
            user.save()
            return redirect('UserApp:Signin')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        jd = json.loads(request.body.decode('utf-8'))
        username = jd['username']
        client_password = jd['password']
        rep = jd['repetitions']
        try:
            user = User.objects.get(username=username)
            message = 'client_password (sent from front) :' + client_password + '<br>'
            message += 'server_password :' + hasher.hash_password(client_password) + '<br>'
            message += 'hashed_password in DB:' + user.password + '<br>'
            message += 'repetitions:' + str(user.repetitions) + '<br>'
            if hasher.check_password(user, client_password):
                user.password = client_password
                user.repetitions = rep - 1
                user.save()
                return HttpResponse("Login successful.<br>" + message)
            elif rep == 0:
                return HttpResponse('your OTP token does not valid anymore please set a new password')
            else:
                return HttpResponse("Invalid username or password.")
        except User.DoesNotExist:
            return HttpResponse("Invalid username or password.")
    else:
        return render(request, 'signin.html')


@csrf_exempt
def repetitions(request):
    if request.method == 'POST':
        jd = json.loads(request.body.decode('utf-8'))
        username = jd['username']
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'repetitions': user.repetitions})
        except User.DoesNotExist:
            return JsonResponse({'repetitions': f'Invalid request-{username}'})
    return JsonResponse({'repetitions': 'Invalid request'})


def home(request):
    return render(request, 'home.html')
