from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError
import logging

class Person(models.Model):
    genders=(
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    prefixes=(
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Miss', 'Miss'),
        ('Dr.', 'Dr.'),
    )
    suffixes=(
        ('Jr.','Jr.'),
        ('Sr.','Sr.'),
        ('Third','Third'),
        ('Fourth','Fourth'),
    )
    marital_statuses=(
        ('Single','Single'),
        ('Married','Married'),
        ('Divorced','Divorced'),
        ('Widowed','Widowed'),
    )
    ethnicities=(
        ('Black','Black'),
        ('White','White'),
        ('Hispanic','Hispanic'),
        ('Asian','Asian'),
        ('Pacific Islander','Pacific Islander'),
        ('Other','Other'),
    )
    #username=models.CharField(max_length=11, unique=True, null=True, blank=True)
    created_on=models.DateTimeField(default=datetime.utcnow())
    updated_on=models.DateTimeField(default=datetime.utcnow())
    is_active=models.BooleanField(default=True)
    is_partner=models.BooleanField("Partner Status", default=False)
    first_name=models.CharField(max_length=30, null=False, blank=False)
    prefix=models.CharField(max_length=10, choices=prefixes, null=True, blank=True)
    last_name=models.CharField(max_length=30, null=False, blank=False)
    middle_name=models.CharField(max_length=30, null=True, blank=True)
    suffix=models.CharField(max_length=10, choices=suffixes, null=True, blank=True)
    dob=models.DateField(auto_now=True)
    gender=models.CharField(max_length=6, choices=genders)
    ethnicity=models.CharField(choices=ethnicities, max_length=50, blank=True, null=True)
    phone=models.ManyToManyField("Phone", null=True, blank=True)
    email=models.ManyToManyField("Email_Address", null=True, blank=True)
    address_1=models.CharField(max_length=30, null=True, blank=True)
    address_2=models.CharField(max_length=30, null=True, blank=True)
    city=models.CharField(max_length=30, null=True, blank=True)
    state=models.CharField(max_length=2, default="TX")
    zip=models.CharField(max_length=10, blank=True, null=True)
    marital_status=models.CharField(max_length=15, choices=marital_statuses, default="Single")
    groups=models.ManyToManyField("Group", null=True, blank=True)
    interests=models.ManyToManyField("Interest", null=True, blank=True)
    occupation_employer=models.CharField(max_length=30, null=True, blank=True)
    notes=models.TextField(null=True, blank=True)
    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)
    class Meta:
        verbose_name_plural="People"

class Group(models.Model):
    name=models.CharField(max_length=30, unique=True, null=False, blank=False)
    is_active=models.BooleanField(default=True)
    created_on=models.DateTimeField(default=datetime.utcnow())
    group_members=models.ManyToManyField(Person, null=True, blank=True)
    parent_group=models.ForeignKey("Group", null=True, blank=True)
    type=models.ForeignKey("Group_Type")
    def __unicode__(self):
        return "%s: %s" % (self.type.name, self.name)

class Group_Type(models.Model):
    name=models.CharField(max_length=30)
    is_active=models.BooleanField(default=True)
    def __unicode__(self):
        return self.name

class Email_Address(models.Model):
    email_address=models.CharField(max_length=30, null=False, blank=False)
    def __unicode__(self):
        return self.email_address
    class Meta:
        verbose_name_plural="Email Addresses"

class Phone(models.Model):
    phone_types=(
        ("Home","Home"),
        ("Mobile","Mobile"),
        ("Work","Work"),
        ("Other","Other"),
    )
    number=models.CharField(max_length=30, null=False, blank=False)
    type=models.CharField(max_length=30, choices=phone_types)
    def __unicode__(self):
        return "%s %s" % (self.number, self.type)
    class Meta:
        verbose_name_plural="Phone Numbers"


class Visitor(Person):
    sources=(
        ('Website','Website'),
        ('Radio','Radio'),
        ('Flier','Flier'),
        ('Friend','Friend'),
        ('Family','Family'),
    )
    heard_by=models.CharField(max_length=30, choices=sources)

class Visit(models.Model):
    visits=(
        ('1','1'),
        ('2','2'),
        ('3','3'),
    )
    date=models.DateField(default=datetime.today())
    person=models.ForeignKey(Person)
    visit_number=models.CharField(max_length=1, choices=visits)
    def __unicode__(self):
        return "%s: %s %s" % (self.date, self.person.first_name, self.person.last_name)

class Interest(models.Model):
    name=models.CharField(max_length=30, null=True, blank=True)
    def __unicode__(self):
        return self.name

class RHF_Registration(models.Model):
    class_statuses=(
        ('Registered', 'Registered'),
        ('Walk-in', 'Walk-in'),
    )
    class_date=models.DateField(null=True, blank=True)
    class_status=models.CharField(max_length=15, choices=class_statuses)
    class_notes=models.TextField(null=True, blank=True)
    person=models.ForeignKey(Visitor)
    def __unicode__(self):
        return "%s: %s %s" % (self.class_date, self.person.first_name, self.person.last_name)
    class Meta:
        verbose_name_plural="RHF Registrations"
        verbose_name="RHF Registration"


class Child(Person):
    mother=models.ForeignKey(Person, related_name='mother', null=True, blank=True)
    father=models.ForeignKey(Person, related_name='father', null=True, blank=True)
    class Meta:
        verbose_name_plural="Children"
        verbose_name="Child"

class Event(models.Model):
    name=models.CharField(max_length=30)
    date=models.DateField(default=datetime.today())
    def __unicode__(self):
        return "%s %s" % (self.date, self.name)

class Task(models.Model):
    task_types=(
        ('Phone Call','Phone Call'),
        ('email','email'),
        ('Meeting','Meeting'),
        ('task4','task4'),
        ('task5','task5'),
    )
    task_status=(
        ('New','New'),
        ('Open','Open'),
        ('Closed','Closed'),
        ('Cancelled','Cancelled'),
        ('Deleted','Deleted'),
    )
    type=models.CharField(max_length=30, choices=task_types)
    status=models.CharField(max_length=30, choices=task_status)
    description=models.TextField(null=True, blank=True)
    person=models.ForeignKey(Person)
    assigned_to=models.ForeignKey(User, related_name="assigned_to", null=True, blank=True)
    submitted_by=models.ForeignKey(User, related_name="submitted_by", null=True, blank=True)
    completed_by=models.ForeignKey(User, related_name="completed_by", null=True, blank=True)
    def __unicode__(self):
        return "%s:  %s" % (self.type, self.person)

class FactKey(models.Model):
    name=models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Fact(models.Model):
    key=models.ForeignKey(FactKey)
    value=models.CharField(max_length=30)
    person=models.ForeignKey(Person)
    def __unicode__(self):
        return "%s : %s" % (self.key.name, self.value)


