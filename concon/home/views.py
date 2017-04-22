# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.http import HttpResponse, HttpResponseRedirect
# get_object_or_404,
# from django.urls import reverse
# from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from forms import SignUpForm


def index(request):

    return render(request, 'home/index.html', {})


def conflict(request):

    return render(request, 'home/conflict.html', {})


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
