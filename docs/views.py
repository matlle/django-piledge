import datetime, random, sha
from django.http import Http404
from django.core.mail import send_mail
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forms import DocForm, CustomUserCreationForm

from docs.models import Doc



""" ===================== Doc Process ====================== """


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
    slug_field = 'doc_slug'


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




""" ========================= User Process ============================ """


def register(request, template_name="docs/authors/signup.html"):
    redirect_at_url = reverse('docs:index')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_at_url)
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ue = postdata.get('username', '')
            pw = postdata.get('password1', '')
            new_user = authenticate(username=ue, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                return HttpResponseRedirect(redirect_at_url)
            
    else:
        form = CustomUserCreationForm()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))





def signin(request):
    redirect_at_url = reverse('docs:index')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_at_url)
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            errors = 'This username doesn\'t exist. Try again please'
            return render_to_response('docs/authors/login.html', locals(), context)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #redirect_at_url = reverse('docs:index')
                return HttpResponseRedirect(redirect_at_url)
            else:
                errors = "You're account is disabled"
        else:
            errors = 'Your username/password is incorrect. Try again please'
            return render_to_response('docs/authors/login.html', locals(), context)
    else:
        return render_to_response('docs/authors/login.html', locals(), context)


@login_required(login_url='docs:signin')
def signout(request):
    logout(request)
    redirect_at_url = reverse('docs:index')
    return HttpResponseRedirect(redirect_at_url)




