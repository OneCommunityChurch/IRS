__author__ = 'jade'
from django.forms import ModelForm
from django import forms
from models import *
from django.template.loader import render_to_string
from datetime import datetime

class SelectWithPop(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("form/popupplus.html", {'field': name})

        return html+popupplus

class MultipleSelectWithPop(forms.SelectMultiple):
    def render(self, name, *args, **kwargs):
        html = super(MultipleSelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("form/popupplus.html", {'field': name})

        return html+popupplus

class Person_Form(ModelForm):
    interests=forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    groups=forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    phone=forms.ModelMultipleChoiceField(queryset=Phone.objects.all(), widget=MultipleSelectWithPop, required=False)
    email=forms.ModelMultipleChoiceField(Email_Address.objects.all(), widget=MultipleSelectWithPop, required=False)
    notes=forms.ModelMultipleChoiceField(Note.objects.all(), widget=MultipleSelectWithPop, required=False)
    medical_conditions=forms.ModelMultipleChoiceField(queryset=MedicalCondition.objects.all(), widget=MultipleSelectWithPop, required=False)
    class Meta:
        model=Person

class newPerson_Form(Person_Form):
    pass

class Visitor_Form(Person_Form):
    questions=forms.ModelMultipleChoiceField(queryset=QuestionAbout.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    visits=forms.ModelMultipleChoiceField(queryset=Visit.objects.all(), widget=MultipleSelectWithPop, required=False)
    class Meta:
        model=Visitor

class newVisitor_Form(newPerson_Form):
    questions=forms.ModelMultipleChoiceField(queryset=QuestionAbout.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    visits=forms.ModelMultipleChoiceField(queryset=Visit.objects.all(), widget=MultipleSelectWithPop, required=False)
    class Meta:
        model=Visitor

class Child_Form(Person_Form):
    class Meta:
        model=Child

class newChild_Form(newPerson_Form):
    parent_guardian=forms.ModelMultipleChoiceField(queryset=Parent_Guardian.objects.all(), widget=MultipleSelectWithPop)
    class Meta:
        model=Child

#add new contact pop-up
class phoneForm(forms.ModelForm):
    class Meta:
        model = Phone

#add new visit pop-up
class visitForm(forms.ModelForm):
    class Meta:
        model = Visit

#add new Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude=('submitted_by', 'completed_by', 'completed_on', )

#add new tag pop-up
class emailForm(forms.ModelForm):
    class Meta:
        model = Email_Address

class noteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude=('created_by', 'created_on',)


class parent_guardian_form(forms.ModelForm):
    class Meta:
       model=Parent_Guardian

class medical_condition_form(forms.ModelForm):
    class Meta:
        model=MedicalCondition

class task_form(forms.ModelForm):
    class Meta:
        model=Task