from django.forms import ModelForm
from django import forms
from docs.models import Doc, Comment
from django.forms.extras.widgets import SelectDateWidget


"""class SignupForm(account.forms.SignupForm):
    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1991)))"""


class DocForm(ModelForm):
    class Meta:
        model = Doc
        fields = ['doc_title', 'doc_description', 'doc_file_name']
