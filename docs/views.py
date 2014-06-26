from django.http import Http404
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from forms import DocForm, UserRegistrationForm

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
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = request.POST['email']
            user.set_password(user.password)
            user.save()
            #ue = postdata.get('email', '')
            #pw = postdata.get('password1', '')
            new_user = authenticate(username=user.username, password=user.password)
            if new_user and new_user.is_active:
                login(request, new_user)
                redirect_at_url = urlresolvers.reverse('index')
                return HttpResponseRedirect(redirect_at_url)
            

    else:
        form = UserCreationForm()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))



def signin(request):
    context = RequestContext(request)
    if request.method == 'POST':
        un = request.POST['username']
        up = request.POST['password']
        user = authenticate(usernae=un, password=up)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("You're account is disabled")
        else:
            #print "Invalid login details " + un + " " + up
            return render_to_response('docs/authors/login.html', {}, context)
    else:
        return render_to_response('docs/authors/login.html', {}, context)







