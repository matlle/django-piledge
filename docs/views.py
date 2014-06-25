from django.http import Http404
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
import forms

from docs.models import Doc



#class LoginView(account.views.LoginView):
    
#    form_class = account.forms.LoginEmailForm


"""class SignupView(account.views.SignupView):

    form_class = forms.SignupForm

    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = self.created_user.get_profile()
        profile.birthdate = form.cleaned_data["birthdate"]
        profile.save()
"""


class IndexView(generic.ListView):
    template_name = 'docs/base/home.html'
    context_object_name = 'latest_doc_list'

    def get_queryset(self):
        """
        Return the last added docs.
        """
        return Doc.objects.order_by('-doc_created_at')
       

class DetailView(generic.DetailView):
    model = Doc
    template_name = 'docs/file/show.html'


class DocCreateView(generic.CreateView):
    model = Doc
    template_name = "docs/file/share.html"
    success_url = "/"
    
    def form_valid(self, form):
        if form.is_valid():
            doc = form.save(commit=False)
            doc.author = self.request.user
            #doc.doc_slug = doc.doc_title
            #doc.save()
        return super(DocCreateView, self).form_valid(form)



