from django.conf.urls import patterns, include, url
from django.contrib.auth import decorators
from django.conf import settings

from docs import views


urlpatterns = patterns('',

    url(r'^$', views.IndexView.as_view(), name='index'),

    #url(r'^signup/$', views.SignupView.as_view(), name="accounts_signup"),

    url(r'^upload$', views.DocCreateView.as_view(), name='upload'),

    url(r'^upload_doc$', views.upload_doc, name='upload_doc'),

    url(r'^doc_thumb$', views.create_doc_thumbnail, name='create_doc_thumbnail'),

    url(r'^(?P<slug>[\w-]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'^SignupAuthUser$', views.register, name='signup'),

    url(r'^Signin$', views.signin, name='signin'),

    url(r'^Logout$', views.signout, name='logout'),

    url(r'^resetpw$', views.change_password, name='change_password'),

    url(r'^resetpw/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.change_password_confirm, name='change_password_confirm'),

    url(r'^success$', views.success, name='success'),

    url(r'^(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
