from django import forms
from web.models import Password

class PasswordsForm(forms.ModelForm):
    class Meta:
        model = Password
        #exclude = ('password',)
    passwords = forms.CharField(widget=forms.Textarea(),)
    