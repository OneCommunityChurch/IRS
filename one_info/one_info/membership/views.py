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
    return render_to_response("membership/index.html", {}, RequestContext(request))

def edit_person(request, id=None):
    if request.method=='POST':
        if id:
            person=Person.objects.get(pk=id)
            form=Person_Form(request.POST, instance=person)
        else:
            form=Person_Form(request.POST)
        if form.is_valid():
            try:
                form.save()
                id = form.instance.id
                return redirect('/membership/view/%s' % id)
            except IndexError:
                flash_message='One or more of the values are out of range.  Please, check the values and try again.'
                return render_to_response("membership/edit_person.html", {"flash": flash_message, "form":form, }, RequestContext(request))
        else:
            flash_message="Please correct the errors below."
            return render_to_response("membership/edit_person.html", {"form":form, "flash": flash_message}, RequestContext(request))
    else:
        try:
            person=Person.objects.get(pk=id)
            form=Person_Form(instance=person)
        except:
            form=Person_Form()
    return render_to_response("membership/edit_person.html", {"form":form}, RequestContext(request))

def view_person(request, id=None):
    return HttpResponse("Cool!")