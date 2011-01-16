from web.models import Password, Source
from web.forms import PasswordsForm
from django.contrib import admin
from django.db import transaction



admin.site.register(Source)

class PasswordAdmin(admin.ModelAdmin):
    form = PasswordsForm
    
    @transaction.commit_manually
    def save_model(self, request, obj, form, change):
        
        # Batch insert from textarea:
        for pw in request.POST['passwords'].split('\r\n'):
            if len(pw) != 0:
                p = Password(password=pw, Source_id=request.POST['Source'])
                p.save()

        # Insert/update one from input text:
        if len(request.POST['password']) > 0:
            obj.password = request.POST['password']
            obj.Source_id = request.POST['Source']
            obj.save()
            
        transaction.commit()

admin.site.register(Password, PasswordAdmin)
