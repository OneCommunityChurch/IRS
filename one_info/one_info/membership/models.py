from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.core.exceptions import ValidationError
import logging
from one_info.settings import *


services=( ('First','First'),
           ('Second','Second'),
           ('Third','Third'),
           ('Fourth','Fourth'),
           ('Saturday','Saturday'),
         )

genders=(
        ('Unknown', 'Unknown'),
        ('Male', 'Male'),
        ('Female', 'Female'),
       )

prefixes=(
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Ms.', 'Ms.'),
        ('Dr.', 'Dr.'),
       )

suffixes=(
        ('Jr.','Jr.'),
        ('Sr.','Sr.'),
        ('Third','Third'),
        ('Fourth','Fourth'),
       )

marital_statuses=(
        ('Unknown','Unknown'),
        ('Single','Single'),
        ('Married','Married'),
        ('Divorced','Divorced'),
        ('Widowed','Widowed'),
       )

ethnicities=(
        ('Unknown','Unknown'),
        ('Black','Black'),
        ('White','White'),
        ('Hispanic','Hispanic'),
        ('Asian','Asian'),
        ('Pacific Islander','Pacific Islander'),
        ('Other','Other'),
       )

class Person(models.Model):
    #username=models.CharField(max_length=11, unique=True, null=True, blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_partner=models.BooleanField("Partner Status", default=True)
    service=models.CharField(max_length=50, choices=services, null=True, blank=True)
    prefix=models.CharField(max_length=10, choices=prefixes, null=True, blank=True)
    first_name=models.CharField(max_length=30, null=False, blank=False)
    middle_name=models.CharField(max_length=30, null=True, blank=True)
    last_name=models.CharField(max_length=30, null=False, blank=False)
    suffix=models.CharField(max_length=10, choices=suffixes, null=True, blank=True)
    dob=models.DateField(default=date(1900,1,1))
    gender=models.CharField(max_length=10, choices=genders, null=True, blank=True)
    ethnicity=models.CharField(choices=ethnicities, max_length=50, blank=True, null=True)
    phone=models.ManyToManyField("Phone", null=True, blank=True)
    email=models.ManyToManyField("Email_Address", null=True, blank=True)
    address_1=models.CharField(max_length=120, null=True, blank=True)
    address_2=models.CharField(max_length=120, null=True, blank=True)
    city=models.CharField(max_length=120, null=True, blank=True)
    state=models.CharField(max_length=2, default="TX")
    zip=models.CharField(max_length=10, blank=True, null=True)
    marital_status=models.CharField(max_length=15, choices=marital_statuses, null=True, blank=True)
    groups=models.ManyToManyField("Group", null=True, blank=True)
    interests=models.ManyToManyField("Interest", null=True, blank=True)
    occupation_employer=models.CharField(max_length=30, null=True, blank=True)
    notes=models.ManyToManyField("Note", null=True, blank=True)
    comments=models.ManyToManyField("Comment", blank=True, null=True, related_name="comments")
    medical_conditions=models.ManyToManyField("MedicalCondition", null=True, blank=True)
    facts=models.ManyToManyField("Fact", null=True, blank=True)
    photo=models.FileField(blank=True, null=True, upload_to="photos")
    def __unicode__(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)
    class Meta:
        verbose_name_plural="People"
        ordering=["last_name", "first_name", "dob"]
        unique_together=("first_name", "last_name", "dob")
    def get_age(self):
        today=datetime.today().date()
        age=(today-self.dob).days/365
        return age
    def get_fullname(self):
        if self.suffix:
            suffix=", %s" % self.suffix
        else:
            suffix=''
        if self.middle_name:
            middle_name="%s " % self.middle_name
        else:
            middle_name=''
        fullname="%s %s%s%s" % (self.first_name, middle_name, self.last_name, suffix)
        return fullname
    def get_primary_phone(self):
        return ", ".join([x.number for x in self.phone.all()])
    def get_primary_email(self):
        return ", ".join([x.email_address for x in self.email.all()])

class Comment(models.Model):
    comment=models.TextField(max_length=256)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    commenter=models.ForeignKey(User)
    def __unicode__(self):
        return "%s: %s" % (self.created_on.date(), self.commenter)

class Group(models.Model):
    name=models.CharField(max_length=30, unique=True, null=False, blank=False)
    is_active=models.BooleanField(default=True)
    created_on=models.DateTimeField(default=datetime.utcnow())
    group_members=models.ManyToManyField(Person, null=True, blank=True)
    parent_group=models.ForeignKey("Group", null=True, blank=True)
    type=models.ForeignKey("Group_Type")
    point_of_contact=models.ForeignKey("Person", related_name="point_of_contact", null=True, blank=True)
    def __unicode__(self):
        return "%s: %s" % (self.type.name, self.name)

    class Meta:
        ordering=['type', 'name']

class Group_Type(models.Model):
    name=models.CharField(max_length=30)
    is_active=models.BooleanField(default=True)
    def __unicode__(self):
        return self.name

class Email_Address(models.Model):
    email_address=models.EmailField()
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
    number=models.CharField(max_length=30)
    type=models.CharField(max_length=30, choices=phone_types, default='Other')
    def __unicode__(self):
        return "%s %s" % (self.number, self.type)
    class Meta:
        verbose_name_plural="Phone Numbers"


class Visitor(Person):
    sources=(
        ('Friend','Friend'),
        ('Family','Family'),
        ('Website','Website'),
        ('Newspaper','Newspaper'),
        ('Radio','Radio'),
        ('Billboard','Billboard'),
        ('Flyer','Flyer'),
        ('Mailer','Mailer'),
    )
    questions=models.ManyToManyField("QuestionAbout", blank=True, null=True)
    other_notes=models.TextField(max_length=100, blank=True, null=True)
    visits=models.ManyToManyField("Visit", blank=True, null=True)
    heard_by=models.CharField(max_length=30, choices=sources, null=True, blank=True)

    def get_last_visit(self):
        try:
           return str(self.visit_set.latest('date').date)
        except:
            return ''
    def get_number_visits(self):
        return self.visit_set.count()

    last_visit=property(get_last_visit)
    number_visits=property(get_number_visits)

class Visit(models.Model):
    date=models.DateField(default=datetime.today())
    person=models.ForeignKey(Visitor)
    service=models.CharField(max_length="30", choices=services)
    def __unicode__(self):
        return "%s: %s %s" % (self.date, self.person.first_name, self.person.last_name)

class Interest(models.Model):
    name=models.CharField(max_length=80)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=["name"]

class QuestionAbout(models.Model):
    name=models.CharField(max_length=80)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering=["name"]
        verbose_name="Question About"
        verbose_name_plural="Questions About"

class RHF_Registration(models.Model):
    class_statuses=(
        ('Registered', 'Registered'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
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
    parent_guardian=models.ManyToManyField("Parent_Guardian", null=True, blank=True)
    class Meta:
        verbose_name_plural="Children"
        verbose_name="Child"

class MedicalCondition(models.Model):
    condition_type=models.CharField(max_length=50)
    condition_value=models.CharField(max_length=50, blank=True, null=True)
    comments=models.TextField(max_length=256, null=True, blank=True)
    def __unicode__(self):
        return "%s %s" % (self.condition_type, self.condition_value)
    class Meta:
        verbose_name="Medical Condition"
        verbose_name_plural="Medical Conditions"


class Parent_Guardian(models.Model):
    types=(
        ('Mother','Mother'),
        ('Father','Father'),
        ('Grandparent','Grandparent'),
        ('Sibling','Sibling'),
        ('Legal Guardian','Legal Guardian'),
        ('Uncle/Aunt','Uncle/Aunt'),
        ('Other Family','Other Family'),
    )
    person=models.ForeignKey(Person)
    type=models.CharField(max_length=30, choices=types)
    def __unicode__(self):
        return "%s: %s" % (self.type, self.person.get_fullname())
    class Meta:
        verbose_name="Parent/Guardian"
        verbose_name_plural="Parents/Guardians"

class Event(models.Model):
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=30)
    event_date=models.DateField(default=datetime.today())
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
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
        ('Deleted','Deleted'),
    )
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    type=models.CharField(max_length=30, choices=task_types)
    status=models.CharField(max_length=30, choices=task_status, default="New")
    description=models.TextField(null=True, blank=True)
    person=models.ForeignKey(Person)
    assigned_to=models.ForeignKey(User, related_name="assigned_to", null=True, blank=True)
    due_date=models.DateField(null=True, blank=True)
    reminder=models.DateTimeField(null=True, blank=True)
    submitted_by=models.ForeignKey(User, related_name="submitted_by", null=True, blank=True)
    completed_by=models.ForeignKey(User, related_name="completed_by", null=True, blank=True)
    completed_on=models.DateTimeField(null=True, blank=True)
    def __unicode__(self):
        return "%s:  %s" % (self.type, self.person)
    def save(self, request=None, *args, **kwargs):
        if request:
            user=request.user
        else:
            user=None
        if self.status=="Completed":
            self.completed_on=datetime.now()
            self.completed_by=user
        if self.status=="New":
            self.submitted_by=user
        super(Task, self).save(*args, **kwargs)


"""
RDF Compaptible Fact Table
-----------------------------
The subject denotes the resource, and the predicate denotes traits or aspects of
the resource and expresses a relationship between the subject and the object.

For Example:   The Sky has the color Blue

Subject:  Sky
predicate:  has the color
object:   blue

"""
class FactSubject(models.Model):
    name=models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class FactPredicate(models.Model):
    name=models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Fact(models.Model):
    subject=models.ForeignKey(FactSubject)
    predicate=models.ForeignKey(FactPredicate)
    object=models.CharField(max_length=30)
    def __unicode__(self):
        return "%s  %s %s" % (self.subject.name, self.predicate, self.object)

class Note(models.Model):
    created_on=models.DateTimeField(auto_now_add=True)
    created_by=models.CharField(User, max_length=80)
    notes=models.TextField(null=True, blank=True)
    def __unicode__(self):
        slug=self.notes[:80]
        return "Note: %s - %s" % (self.created_on, slug)

