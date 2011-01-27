from web.models import Strength, PasswordUnique, Password, Source
from web.forms import PasswordsForm
from django.contrib import admin
from django.db import transaction



admin.site.register(Source)
admin.site.register(PasswordUnique)
admin.site.register(Strength)
admin.site.register(Password)
#TODO: Too many weird shit here... You should rewrite this somwhere else...
#class PasswordAdmin(admin.ModelAdmin):
#    form = PasswordsForm
#    
#    
#    @transaction.commit_manually
#    def save_model(self, request, obj, form, change):
#        
#        # Batch insert from textarea:
#        for pw in request.POST['passwords'].split('\r\n'):
#            if len(pw) != 0:
#                p = Password(password=pw, source_id=request.POST['source'])
#                p.save()
#
#        # Insert/update one from input text:
#        if len(request.POST['password']) > 0:
#            obj.password = request.POST['password']
#            obj.source_id = request.POST['source']
#            obj.save()
#            
#        transaction.commit()
#
#admin.site.register(Password, PasswordAdmin)
