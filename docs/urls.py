from django.conf.urls import patterns, include, url
from django.contrib.auth import decorators
from django.conf import settings

from docs import views

urlpatterns = patterns('',

    url(r'^$', views.IndexView.as_view(), name='index'),

    #url(r'^signup/$', views.SignupView.as_view(), name="accounts_signup"),

    url(r'^upload$', views.DocCreateView.as_view(), name='upload'),

    url(r'^(?P<slug>[\w-]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'^SignupAuthUser$', views.register, name='signup'),

    url(r'^Signin$', views.signin, name='signin'),

    url(r'^(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
