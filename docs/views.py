import datetime, random, sha
import django.utils.simplejson as json
from django.http import Http404
from django.core.mail import send_mail
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
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



def update_progress_direct(request, message):
    from django.core.cache import cache
    try:
        cache_key = "%s_%s" % (request['addr'], request['pid'])
        data = cache.get(cache_key)
        if data:
            data['status'] = message
            cache.set(cache_key, data)
        else:
            cache.set(cache_key, {
                'length': 100,
                'uploaded': 100,
                'status': message
            })
    except:
        pass



def upload_doc(request):
    request.upload_handlers.insert(0, ProgressBarUploadHandler())
    return _upload_file_view(request)
 

def create_doc_thumbnail(request):
    if request.method == 'POST' and request.is_ajax():
        from wand.image import Image
        form = DocForm(request.POST)
        titleD = request.FILE['doc_file_name']
        msg = "Ajax works!"
        """with Image(filename=doc_name[0]) as doc_thumb:
            doc_thumb.save(filename="/temp.jpg")
        with Image(filename="/temp.jpg") as doc_thumb:
            doc_thumb.resize(200, 100)
            doc_thumb.save(filename="/thumbnail_resize.jpg")
        """
    return HttpResponse(titleD)

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
            ierrors = 'This username doesn\'t exist. Try again please'
            return render_to_response('docs/authors/login.html', locals(), context)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(redirect_at_url)
            else:
                ierrors = "You're account is disabled"
        else:
            ierrors = 'Your username/password is incorrect. Try again please'
            return render_to_response('docs/authors/login.html', locals(), context)
    else:
        return render_to_response('docs/authors/login.html', locals(), context)


@login_required(login_url='docs:signin')
def signout(request):
    logout(request)
    redirect_at_url = reverse('docs:index')
    return HttpResponseRedirect(redirect_at_url)




def change_password(request):
    return password_reset(request, template_name='reset.html',
                          email_template_name='reset_email.html',
                          subject_template_name='reset_subject.txt',
                          post_reset_redirect=reverse('docs:success'))


def change_password_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='reset_confirm.html',
    uidb36=uidb36, token=token, post_reset_redirect=reverse('docs:success'))



def success(request):
    context = RequestContext(request)
    return render_to_response('docs/authors/success.html', {}, context)



