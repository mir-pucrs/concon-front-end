from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from views import IndexView, ProfileView

app_name = 'home'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^conflict/$', views.conflict, name='conflict'),
    url(r'^intro/$', TemplateView.as_view(template_name='home/intro.html'), name='intro'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<con_id>\d+)/$', views.delete_contract, name='delete-contract'),
    url(r'^contract/(?P<con_id>\d+)/$', views.contract, name='contract'),
    url(r'^model_description/$', TemplateView.as_view(template_name='home/introducing_models.html'), name='model_description'),
]
