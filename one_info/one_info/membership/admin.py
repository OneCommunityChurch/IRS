__author__ = 'jade'

from django.contrib import admin
from one_info.membership.models import *

#class AnalystAdmin(admin.ModelAdmin):
#    list_display = ('first_name', 'last_name', 'analyst_id')
    
#class TPCFAdmin(admin.ModelAdmin):
#    pass

#admin.site.register(Analyst, AnalystAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name', 'is_partner', 'is_active')

class TaskAdmin(admin.ModelAdmin):
    list_display=('type', 'status', 'description', 'person', 'assigned_to')

class VisitAdmin(admin.ModelAdmin):
    list_display = ('date', 'person', 'service')
    list_filter = ('date', 'service',)

admin.site.register(Person, PersonAdmin)
admin.site.register(Group)
admin.site.register(Group_Type)
admin.site.register(Email_Address)
admin.site.register(Phone)
admin.site.register(Visitor)
admin.site.register(Child)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Interest)
admin.site.register(RHF_Registration)
admin.site.register(Event)
admin.site.register(Task, TaskAdmin)
admin.site.register(FactSubject)
admin.site.register(FactPredicate)
admin.site.register(Fact)
admin.site.register(Parent_Guardian)
admin.site.register(MedicalCondition)
admin.site.register(Comment)
admin.site.register(QuestionAbout)
admin.site.register(Note)

