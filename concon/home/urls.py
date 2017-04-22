from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^conflict/$', views.conflict, name='conflict'),
    url(r'^intro/$', views.intro, name='intro'),
    url(r'^about/$', views.about, name='about'),
    # url(r'^login/$', views.login_page, name='login'),
    url(r'^register/$', views.register, name='register'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
