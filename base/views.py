from django.shortcuts import render, redirect
from .models import User, Event, Submission
from .forms import SubmissionForm, CustomUserCreationForm, EditUserForm
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        user = authenticate(
            email = request.POST['email'],
            password = request.POST['password']  
            )
        if user is not None:
            login(request, user)
            messages.info(request, "You have successfully logged in !")
            return redirect('home')
        else:
            messages.error(request, "Email or Password is incorrect !")
    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def register_page(request):
    page = 'register'
    form = CustomUserCreationForm() 

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, "User account was created.")
            return redirect('home')
        else:
            messages.error(request, "An error has occured during registration !!")

    context = {'page':page, 'form':form}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully !!")
    return redirect('login')


def home_page(request):
    limit = request.GET.get('limit')
    if limit == None:
        limit = 20
    limit = int(limit)

    events = Event.objects.all()
    users = User.objects.filter(hackathon_participant=True)
    count = users.count()

    page = request.GET.get('page')
    paginator = Paginator(users, 4)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        users = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        users = paginator.page(page)

    pages = list(range(1, (paginator.num_pages + 1)))

    users = users[0:20]

    context = {'users': users, 'events': events, 'count':count, 'paginator':paginator, 'pages':pages}
    return render(request, 'base/home.html', context)


@login_required(login_url='/login')
def account_page(request):
    user = request.user
    context = {'user':user}
    return render(request, 'base/account.html', context)


@login_required(login_url='/login')
def update_user_account(request):
    form = EditUserForm(instance=request.user)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/update_user_account.html', context)


@login_required(login_url='/login')
def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def reset_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            new_password = make_password(password1)
            request.user.password = new_password
            request.user.save()
            messages.success(request, "You have successfully reset your password !!")
            return redirect('account')
        else:
            messages.error(request, "Your password1 & password2 does not matched !!")

    return render(request, 'base/reset_password.html')


import time
from datetime import datetime

def event_page(request, pk):
    event = Event.objects.get(id=pk)

    present = datetime.now().timestamp()
    deadline = event.registration_deadline.timestamp()
    post_deadline = (present > deadline)

    registered = False
    submitted = False

    if request.user.is_authenticated:
        registered = request.user.events.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()

    context = {'event':event, 'registered':registered, 'submitted':submitted, 'post_deadline':post_deadline}
    return render(request, 'base/event.html', context)


@login_required(login_url='/login')
def registration_confirmation(request, pk):
    et = Event.objects.get(id=pk)

    if request.method == 'POST':
        et.participants.add(request.user)
        return redirect('event', pk=et.id)

    return render(request, 'base/registration_confirmation.html', {'et':et})


@login_required(login_url='/login')
def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    form = SubmissionForm()

    if request.method == 'POST':
        form = SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()

            return redirect('account')    
    
    context = {'event':event, 'form':form}
    return render(request, 'base/submit_form.html', context)
 

@login_required(login_url='/login')
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse("You can't do this !!!")

    event = submission.event
    form = SubmissionForm(instance=submission)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form, 'event':event}

    return render(request, 'base/submit_form.html', context)