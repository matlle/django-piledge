from django.forms import ModelForm
from django import forms
from docs.models import Doc, Comment
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget


"""class SignupForm(account.forms.SignupForm):
    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1991)))"""


class DocForm(ModelForm):
    class Meta:
        model = Doc
        fields = ['doc_title', 'doc_description', 'doc_file_name']


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


"""class UserLoginForm(ModelForm):
    username=forms.CharField(label=_(u"username"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
"""
