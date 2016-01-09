from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from StudyGroup.views import index
from StudyGroup.views import group
from StudyGroup.views import user
from StudyGroup.views import group_member_inf
from StudyGroup.views import userno
from StudyGroup.views import getcalendarevent
from StudyGroup.views import postcalendarevent
from StudyGroup.views import deletecalendarevent
from StudyGroup.views import get_group_news
from StudyGroup.views import post_group_news
from StudyGroup.views import get_group_materials
from StudyGroup.views import post_group_materials
from StudyGroup.views import send_mail
from StudyGroup.views import get_mail
from StudyGroup.views import get_mission

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^index',index),
	url(r'^$', index),
	url(r'^group/(?P<group_id>[0-9]+)/$',group),
	url(r'^user/(?P<user_id>[0-9]+)/$',user),
	url(r'^group/(?P<group_id>[0-9]+)/member_inf/$',group_member_inf),
	url(r'^userno/(?P<user_id>[0-9]+)/$',userno),
	url(r'^group/(?P<group_id>[0-9]+)/calendar/$',getcalendarevent),
	url(r'^postcalendarevent/(?P<group_id>[0-9]+)/$',postcalendarevent),
	url(r'^deletecalendarevent/(?P<group_id>[0-9]+)/$',deletecalendarevent),
	url(r'^get_group_news/(?P<group_id>[0-9]+)/$',get_group_news),
	url(r'^post_group_news/(?P<group_id>[0-9]+)/$',post_group_news),
	url(r'^static/(?P<path>.*)$', views.serve),
	url(r'^get_group_materials/(?P<group_id>[0-9]+)/$',get_group_materials),
	url(r'^post_group_materials/(?P<group_id>[0-9]+)/$',post_group_materials),
	url(r'^send_mail/(?P<group_id>[0-9]+)/$',send_mail),
	url(r'^get_mail/(?P<user_id>[0-9]+)/$',get_mail),
	url(r'^get_mission/(?P<user_id>[0-9]+)/$',get_mission),
]
 
urlpatterns += staticfiles_urlpatterns()