__author__ = 'jade'

from django.contrib import admin
from one_info.membership.models import *

#class AnalystAdmin(admin.ModelAdmin):
#    list_display = ('first_name', 'last_name', 'analyst_id')
    
#class TPCFAdmin(admin.ModelAdmin):
#    pass

#admin.site.register(Analyst, AnalystAdmin)
admin.site.register(Person)
admin.site.register(Group)
admin.site.register(Group_Type)
admin.site.register(Email_Address)
admin.site.register(Phone)
admin.site.register(Visitor)
admin.site.register(Child)
admin.site.register(Visit)
admin.site.register(Interest)
admin.site.register(RHF_Registration)
admin.site.register(Event)


