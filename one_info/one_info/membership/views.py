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
from django.contrib.auth.views import login, logout
from django.contrib import auth
from urlparse import urlsplit
from django.utils.html import escape
from datetime import datetime, date
import xlwt, pytz

def index(request):
    return render_to_response("membership/index.html", {}, RequestContext(request))

def logout_view(request):
    logout(request)
    return redirect("/membership")

@login_required(login_url="/accounts/login/")
def edit_person(request, id=None):
    if request.method=='POST':
        if id:
            person=Person.objects.get(pk=id)
            form=Person_Form(request.POST, instance=person)
            flash_message="Editing Existing Partner"
        else:
            form=newPerson_Form(request.POST)
            flash_message="Adding New Partner"
        if form.is_valid():
            try:
                form.save()
                id = form.instance.id
                flash_message="Partner info successfully saved!"
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
            tasks=Task.objects.filter(person=person)
            notes=Note.objects.filter(person=person)
            form=Person_Form(instance=person)
            flash_message="Editing Partner"
        except:
            form=newPerson_Form()
            notes=None
            flash_message="Adding New Partner"
            tasks=None
    return render_to_response("membership/edit_person.html", {"form":form, "tasks": tasks, "notes": notes, "flash": flash_message}, RequestContext(request))


login_required(login_url="/accounts/login/")
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
            notes=Note.objects.filter(person=person)
            tasks=Task.objects.filter(person=person)
            flash_message="Editing Existing Visitor"
        except:
            form=newVisitor_Form()
            notes=None
            tasks=None
            flash_message="Adding New Vistor"
    return render_to_response("membership/edit_visitor.html", {"form":form, "notes": notes, "tasks": tasks,
                                                               "flash":flash_message}, RequestContext(request))


@login_required(login_url="/accounts/login/")
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

@login_required(login_url="/accounts/login/")
def view_person(request, id=None):
    return render_to_response("membership/test.html", {"form":{}}, RequestContext(request))

@login_required()
def view_people(request, person_type=None, start=0):
    if person_type=='partners':
        people=Person.objects.filter(is_active=True, is_partner=True).order_by("-updated_on")
        flash_message="Partners"
    elif person_type=='visitors':
        people=Visitor.objects.filter(is_active=True).order_by("-updated_on")
        flash_message="Visitors"
    elif person_type=='children':
        people=Child.objects.filter(is_active=True).order_by("-updated_on")
        flash_message="Children"
    elif person_type=="active":
        people=Person.objects.filter(is_active=True).order_by("-updated_on")
        flash_message="Default"
    else:
        people=Person.objects.all().order_by("-updated_on")
        flash_message="All People"
	paginator=Paginator(people, 150)
	try:
	    page=int(request.GET.get('page', '1'))
    except ValueError:
        page=1
    try:
        people=paginator.page(page)
    except (EmptyPage, InvalidPage):
        people=paginator.page(paginator.num_pages)
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

@login_required(login_url="/accounts/login/")
def task_list(request):
    tasks=Task.objects.all().order_by("-updated_on")
    flash_message="All Tasks"
    return render_to_response("membership/view_tasks.html", {"tasks":tasks, "flash":flash_message}, RequestContext(request))

@login_required(login_url="/accounts/login/")
def edit_task(request, id=None):
    if request.method=='POST':
        if id:
            task=Task.objects.get(pk=id)
            form=TaskForm(request.POST, instance=task)
            flash_message="Editing Existing Task"
        else:
            form=TaskForm(request.POST)
            flash_message="Adding New Task"
        if form.is_valid():
            try:
                form.save()
                id = form.instance.id
                flash_message="Task info successfully saved!"
                return redirect('/membership/tasks')
            except IndexError:
                flash_message='One or more of the values are out of range.  Please, check the values and try again.'
                return render_to_response("membership/edit_task.html", {"flash": flash_message, "form":form, }, RequestContext(request))
        else:
            flash_message="Please correct the errors below."
            return render_to_response("membership/edit_task.html", {"form":form, "flash": flash_message}, RequestContext(request))
    else:
        try:
            task=Task.objects.get(pk=id)
            form=TaskForm(instance=task)
            flash_message="Editing Task"
        except:
            form=TaskForm()
            flash_message="Adding New Task"
    return render_to_response("membership/edit_task.html", {"form":form, "flash": flash_message}, RequestContext(request))

#@login_required(login_url="/accounts/login/")
def visitorReport(request):
    visitors=Visitor.objects.all().order_by("-created_on")
    return render_to_response("membership/visitor_report.html", {"visitors": visitors}, RequestContext(request))


def newPhone(request):
    return handlePopAdd(request, phoneForm, 'phone')

def newVisit(request):
    return handlePopAdd(request, visitForm, 'visit')

def newNote(request):
    return handlePopAdd(request, noteForm, 'notes')

def newEmail(request):
    return handlePopAdd(request, emailForm, 'email')

def newParentGuardian(request):
    return handlePopAdd(request, parent_guardian_form, 'parent_guardian')

def newMedicalCondition(request):
    return handlePopAdd(request, medical_condition_form, 'medical_conditions')

def newTask(request):
    return handlePopAdd(request, task_form, 'task')

def visitor_excel(request):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='mm/dd/yyyy hh:mm')
    date_style = xlwt.easyxf(num_format_str='mm/dd/yyyy')

    values_list = Visitor.objects.all().values_list()

    for row, rowdata in enumerate(values_list):
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                style = datetime_style
                val=val.replace(tzinfo=None)
            elif isinstance(val, date):
                style = date_style
            else:
                style = default_style

            sheet.write(row, col, val, style=style)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=visitors.xls'
    book.save(response)
    return response

def visitor_xls(request):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('visitor report')

    default_style = xlwt.Style.default_style
    datetime_style = xlwt.easyxf(num_format_str='mm/dd/yyyy hh:mm')
    date_style = xlwt.easyxf(num_format_str='mm/dd/yyyy')

    visitors = Visitor.objects.all()

    def write_header():
        #sheet.write(row, col, value)
        sheet.write(0, 0, 'Title')
        sheet.write(0, 1, 'First Name')
        sheet.write(0, 2, 'Last Name')
        sheet.write(0, 3, 'Email')
        sheet.write(0, 4, 'Phone')
        sheet.write(0, 5, 'Gender')
        sheet.write(0, 6, 'Age')
        sheet.write(0, 7, 'Marital Status')
        sheet.write(0, 8, '# Visits')
        sheet.write(0, 9, 'Date of Last Visit')

    write_header()

    for row, visitor in enumerate(visitors):
        title=visitor.prefix
        first_name = visitor.first_name
        last_name =  visitor.last_name
        email=visitor.get_primary_email()
        phone = visitor.get_primary_phone()
        gender=visitor.gender
        if visitor.get_number_visits()>0:
            number_of_visits = visitor.get_number_visits()
        else:
            number_of_visits=1
        if visitor.get_last_visit():
            last_visit=visitor.get_last_visit()
        else:
            d=visitor.created_on.replace(tzinfo=None)
            last_visit="%s-%s-%s" % (d.year, str(d.month).zfill(2), str(d.day).zfill(2))
        if visitor.get_age()>0 and visitor.get_age()<100:
            age=visitor.get_age()
        else:
            age='unknown'
        marital_status=visitor.marital_status

        sheet.write(row+1, 0, title)
        sheet.write(row+1, 1, first_name)
        sheet.write(row+1, 2, last_name)
        sheet.write(row+1, 3, email)
        sheet.write(row+1, 4, phone)
        sheet.write(row+1, 5, gender)
        sheet.write(row+1, 6, age)
        sheet.write(row+1, 7, marital_status)
        sheet.write(row+1, 8, number_of_visits)
        sheet.write(row+1, 9, last_visit)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=visitors.xls'
    book.save(response)
    return response
