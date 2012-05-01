# Create your views here.
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from forms import *
from django.template import RequestContext
from django.core.paginator import *
from django.db.models import Q
from models import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from urlparse import urlsplit

def index(request):
    return HttpResponse("Hello World")