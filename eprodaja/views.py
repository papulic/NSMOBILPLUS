# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .forms import UserForm



def index(request):
    user = None
    if request.user.is_authenticated():
        user = request.user
    return render(request, 'eprodaja/index.html', {'user': user})
