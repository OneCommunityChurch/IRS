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
from django.utils.html import escape

def index(request):
    return render_to_response("membership/index.html", {}, RequestContext(request))

def edit_person(request, id=None):
    if request.method=='POST':
        if id:
            person=Person.objects.get(pk=id)
            form=Person_Form(request.POST, instance=person)
            flash_message="Editing Existing Member"
        else:
            form=newPerson_Form(request.POST)
            flash_message="Adding New Member"
        if form.is_valid():
            try:
                form.save()
                id = form.instance.id
                flash_message="Member info successfully saved!"
                return redirect('/membership/view/partners')
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
            flash_message="Editing Member"
        except:
            form=newPerson_Form()
            flash_message="Adding New Member"
    return render_to_response("membership/edit_person.html", {"form":form, "flash": flash_message}, RequestContext(request))


def edit_visitor(request, id=None):
    if request.method=='POST':
        if id:
            person=Visitor.objects.get(pk=id)
            form=Visitor_Form(request.POST, instance=person)
            flash_message="Editing Existing Visitor"
        else:
            form=newVisitor_Form(request.POST)
            flash_message="Adding New Visitor"
        if form.is_valid():
            try:
                form.save()
                id = form.instance.id
                return redirect('/membership/view/visitors')
            except IndexError:
                flash_message='One or more of the values are out of range.  Please, check the values and try again.'
                return render_to_response("membership/edit_visitor.html", {"flash": flash_message, "form":form, }, RequestContext(request))
        else:
            flash_message="Please correct the errors below."
            return render_to_response("membership/edit_visitor.html", {"form":form, "flash": flash_message}, RequestContext(request))
    else:
        try:
            person=Visitor.objects.get(pk=id)
            form=Visitor_Form(instance=person)
            flash_message="Editing Existing Visitor"
        except:
            form=newVisitor_Form()
            flash_message="Adding New Vistor"
    return render_to_response("membership/edit_visitor.html", {"form":form, "flash":flash_message}, RequestContext(request))


def edit_child(request, id=None):
    if request.method=='POST':
        if id:
            person=Child.objects.get(pk=id)
            form=Child_Form(request.POST, instance=person)
            flash_message="Editing Existing Child"
        else:
            form=newChild_Form(request.POST)
            flash_message="Adding New Child"
        if form.is_valid():
            try:
                form.save()
                id = form.instance.id
                return redirect('/membership/view/children')
            except IndexError:
                flash_message='One or more of the values are out of range.  Please, check the values and try again.'
                return render_to_response("membership/edit_child.html", {"flash": flash_message, "form":form, }, RequestContext(request))
        else:
            flash_message="Please correct the errors below."
            return render_to_response("membership/edit_child.html", {"form":form, "flash": flash_message}, RequestContext(request))
    else:
        try:
            person=Child.objects.get(pk=id)
            form=Child_Form(instance=person)
            flash_message="Editing Existing Child"
        except:
            form=newChild_Form()
            flash_message="Adding New Child"
    return render_to_response("membership/edit_child.html", {"form":form, "flash": flash_message}, RequestContext(request))

def view_person(request, id=None):
    return render_to_response("membership/test.html", {"form":{}}, RequestContext(request))

def view_people(request, person_type=None):
    if person_type=='partners':
        people=Person.objects.filter(is_active=True, is_partner=True)
        flash_message="Partners"
    elif person_type=='visitors':
        people=Visitor.objects.filter(is_active=True)
        flash_message="Visitors"
    elif person_type=='children':
        people=Child.objects.filter(is_active=True)
        flash_message="Children"
    else:
        people=Person.objects.filter(is_active=True)
        flash_message="Default"
    return render_to_response("membership/view_people.html", {"people":people, "person_type": person_type, "flash":flash_message}, RequestContext(request))

def handlePopAdd(request, addForm, field):
    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            try:
                newObject = form.save()
            except forms.ValidationError, error:
                newObject = None
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                                    (escape(newObject._get_pk_val()), escape(newObject)))

    else:
        form = addForm()

    pageContext = {'form': form, 'field': field}
    return render_to_response("form/pop-up.html", pageContext, RequestContext(request))

def newPhone(request):
    return handlePopAdd(request, phoneForm, 'phone')

def newEmail(request):
    return handlePopAdd(request, emailForm, 'email')

def newParentGuardian(request):
    return handlePopAdd(request, parent_guardian_form, 'parent_guardian')

def newMedicalCondition(request):
    return handlePopAdd(request, medical_condition_form, 'medical_conditions')