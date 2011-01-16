from web.models import Password, Source
from web.forms import PasswordsForm
from django.contrib import admin
from django.forms import forms
from django.db import transaction



admin.site.register(Source)

# TODO: Disable error checking -- create a custom form for the adming...
class PasswordAdmin(admin.ModelAdmin):
    form = PasswordsForm
    
    @transaction.commit_manually
    def save_model(self, request, obj, form, change):
        if(change == False):
            
            for pw in request.POST['passwords'].split('\n'):
                p = Password(password=pw, Source_id=request.POST['Source'])
                p.save()
        else:
            # Batch insert is not available when editing:
            obj.password = request.POST['passwords']
            obj.Source_id = request.POST['Source']
            obj.save()
        transaction.commit()
            
            
    # Change the password input to textarea:
    # TODO: don't do this while in edit mode
#    def formfield_for_dbfield(self, db_field, **kwargs):
#        formfield = super(PasswordAdmin, self).formfield_for_dbfield(db_field, **kwargs)
#        if db_field.name == 'password':
#            formfield.widget = forms.Textarea()
#        return formfield

admin.site.register(Password, PasswordAdmin)
