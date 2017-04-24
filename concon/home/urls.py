from django.conf.urls import url
from django.views.generic import TemplateView
import views
from views import IndexView, ProfileView

app_name = 'home'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^conflict/$', views.conflict, name='conflict'),
    url(r'^intro/$', TemplateView.as_view(template_name='home/intro.html'), name='intro'),
    url(r'^about/$', TemplateView.as_view(template_name='home/about.html'), name='about'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<con_id>)/$', views.delete_contract, name='delete-contract')
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
