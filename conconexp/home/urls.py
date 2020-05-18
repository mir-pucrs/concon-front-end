from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from views import IndexView, ProfileView

app_name = 'home'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^conflict/$', views.conflict, name='conflict'),
    url(r'^conflict/(?P<conf_id>\d+)/(?P<model_name>[a-z]+)/$', views.delete_conflict, name='delete_conflict'),
    url(r'^intro/$', TemplateView.as_view(template_name='home/intro.html'), name='intro'),
    url(r'^contact/$', TemplateView.as_view(template_name='home/contact.html'), name='contact'),
    url(r'^terms/$', TemplateView.as_view(template_name='home/terms.html'), name='terms'), 
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<con_id>\d+)/$', views.delete_contract, name='delete-contract'),
    url(r'^contract/(?P<con_id>\d+)/$', views.contract, name='contract'),
    url(r'^contract/(?P<con_id>\d+)/(?P<model_name>[a-z]+)/$', views.contract, name='contract_2'),
    url(r'^model_description/$', TemplateView.as_view(template_name='home/introducing_models.html'), name='model_description'),
    url(r'^new_conflicts/$', views.new_conflicts, name='new_conflicts'),
    url(r'^delete_conf/$', views.delete_conf, name='delete_conf'),
    url(r'^submit_conf/$', views.submit_conf, name='submit_conf'),
]
