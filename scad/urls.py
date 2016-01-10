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
from StudyGroup.views import get_group_thoughts
from StudyGroup.views import post_group_thoughts
from StudyGroup.views import post_group_thought_reply
from StudyGroup.views import post_file
from StudyGroup.views import post_mission
from StudyGroup.views import check_Name
from StudyGroup.views import set_mail_read
from StudyGroup.views import get_my_group

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
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
	url(r'^set_mail_read/(?P<user_id>[0-9]+)/$',set_mail_read),
	url(r'^get_mail/(?P<user_id>[0-9]+)/$',get_mail),
	url(r'^get_mission/(?P<user_id>[0-9]+)/$',get_mission),
	url(r'^get_group_thoughts/(?P<group_id>[0-9]+)/$', get_group_thoughts),
	url(r'^post_group_thoughts/(?P<group_id>[0-9]+)/$', post_group_thoughts),
	url(r'^post_group_thought_reply/(?P<group_id>[0-9]+)/$', post_group_thought_reply),
	url(r'^post_file/(?P<group_id>[0-9]+)/$', post_file),
	url(r'^post_mission/$',post_mission),
	url(r'^check_Name/(?P<mission_no>[0-9]+)/$',check_Name),
	url(r'^get_my_group/(?P<user_id>[0-9]+)/$',get_my_group),
]
 
urlpatterns += staticfiles_urlpatterns()