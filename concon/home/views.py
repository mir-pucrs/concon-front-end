# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.http import HttpResponse    # HttpResponseRedirect
# get_object_or_404,
# from django.urls import reverse
# from django.views import generic
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from forms import SignUpForm
from forms import UploadFileForm
from scripts import insert_contract
from django.contrib.auth.models import User


def index(request):

    return render(request, 'home/index.html', {})


def conflict(request):

    if request.method == 'POST' and request.FILES['upfile']:
        up_file = request.FILES['upfile']
        fs = FileSystemStorage()
        filename = fs.save(up_file.name, up_file)
        uploaded_file_url = fs.url(filename)
        username = request.user.username
        user_id = User.objects.get(username=username).pk
        path = settings.BASE_DIR + uploaded_file_url
        insert_contract(path, user_id)

        return render(request, 'home/conflict.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'home/conflict.html')

def intro(request):

    return render(request, 'home/intro.html', {})


def about(request):

    return render(request, 'home/about.html', {})


def login_page(request):

    return render(request, 'home/login.html', {})


def register(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'home/register.html', {'form': form})
