__author__ = 'jade'
from django.forms import ModelForm
from django import forms
from models import *

class Person_Form(ModelForm):
    class Meta:
        model=Person

class Visitor_Form(ModelForm):
    class Meta:
        model=Visitor

class Child_Form(ModelForm):
    class Meta:
        model=Child

        
