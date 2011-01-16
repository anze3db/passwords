from web.models import Password, Source
from django.contrib import admin
from django.forms import forms



admin.site.register(Source)

# TODO: Disable error checking -- create a custom form for the adming...
class PasswordAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if(change == False):
            # TODO: Find a faster way of doing batch inserts:
            for pw in request.POST['password'].split('\n'):
                p = Password(password=pw, Source_id=request.POST['Source'])
                p.save()
        else:
            # Batch insert is not available when editing:
            obj.password = request.POST['password']
            obj.Source_id = request.POST['Source']
            obj.save()
            
            
    # Change the password input to textarea:
    # TODO: don't do this if your while in edit mode
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(PasswordAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'password':
            formfield.widget = forms.Textarea()
        return formfield

admin.site.register(Password, PasswordAdmin)
