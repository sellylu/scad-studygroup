'''
from .models import Greeting

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
'''
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import time
import datetime
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


@csrf_exempt
def index(request):
	if request.method == 'POST':
		# build a group
		if 'group_name' in request.POST:
			creator = request.POST['creator_id']
			cursor = connection.cursor()
			selectsql = "SELECT * FROM user WHERE user_id = '%s'" %(creator)
			cursor.execute(selectsql)
			user_data = cursor.fetchone()
			
			if(len(user_data)) > 0:
				user_no = user_data[0]
				str_user_no = str(user_no)+','
				user_join_group = user_data[4]
				
				group_name = request.POST['group_name']
				group_name = strcheck(group_name)
				intro = request.POST['intro']
				intro = strcheck(intro)
				private = int(request.POST['private'])
				finished_time = request.POST['finished_time']
				t = time.time()
				created_time = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')
				member_limit = int(request.POST['member_limit'])
				member_num = 1
				group_id = request.POST['group_id']
				
				# insert group into study_group
				insertNewGroupInto_Study_Group_sql = "INSERT INTO study_group(group_member,group_id,group_name,created_time,member_limit,member_num,intro,private,creator,finished_time) " \
					"VALUES ('%s','%s','%s','%s','%d','%d','%s','%d','%s','%s')" %(str_user_no,group_id,group_name,created_time,member_limit,member_num,intro,private,creator,finished_time)
				cursor.execute(insertNewGroupInto_Study_Group_sql)
				
				# get the group_no
				get_group_created_no = "SELECT (no) FROM study_group WHERE group_id = '%s'" %(group_id)
				cursor.execute(get_group_created_no)
				group_created_no = cursor.fetchone()
				
				user_join_group = user_join_group + str(group_created_no[0]) + ','
				
				# insert the group no to the user
				update_creator_join_group_sql = "UPDATE user SET created_achieve=1,join_group = '%s' WHERE no = '%d' " %(user_join_group,user_no)
				cursor.execute(update_creator_join_group_sql)
		
				return HttpResponseRedirect('/group/{}'.format(group_id))
			
			else:
				#handle no this user's id in database
				print('hh')

		# login
		elif 'user_id' in request.POST:
			id = request.POST['user_id']
			email = request.POST['user_email']
			name = request.POST['user_name']
			cursor = connection.cursor()
			selectsql = "SELECT * FROM user WHERE user_id = '%s'" %(id)
			cursor.execute(selectsql)
			user_data = cursor.fetchall()
			cursor2 = connection.cursor()
			if len(user_data) == 0:
				insertsql = "INSERT INTO user(name,user_id,email,login_cnt) VALUES ('%s','%s','%s',1)" %(name,id,email)
				cursor2.execute(insertsql)
			else:
				updatesql = "UPDATE user SET login_cnt = login_cnt + 1 WHERE user_id = '%s'" % (id)
				cursor2.execute(updatesql)
			return HttpResponseRedirect("/")
	
	if request.method == 'GET':
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM study_group")
		group_data = cursor.fetchall()
		data_list = []
		for x in group_data:
			group = {
				'group_id': x[1],
				'group_name':x[2],
				'created_time':x[3],
				'finished_time':x[4],
				'member_num':x[5],
				'member_limit':x[6],
				'group_member':x[7],
				'intro': x[8],
				'private':x[9],
				'creator': x[10]
			}
			data_list.append(group)
		return render(request, 'index.html', {'group_data':data_list})


@csrf_exempt
def group(request,group_id):
	if request.method == 'GET':
		cursor = connection.cursor()
		selectsql = "SELECT * FROM study_group WHERE group_id = '%s'" %(group_id)
		cursor.execute(selectsql)
		group_data = cursor.fetchone()
		
		if group_data:
			group = {
				'group_id': group_data[1],
					'group_name':group_data[2],
					'created_time':group_data[3],
					'finished_time':group_data[4],
					'member_num':group_data[5],
					'member_limit':group_data[6],
					'group_member':group_data[7],
					'intro': group_data[8],
					'private':group_data[9],
					'creator': group_data[10]
			}
			return render(request,'group.html',{'group_page_data':group})
		else:    # no this group
			raise PermissionDenied

	#join into a group
	if request.method == 'POST':
		if 'join_id' in request.POST:
			join_id = request.POST['join_id']
			group_id = request.POST['group_id']
			
			cursor = connection.cursor()
			getgroupnosql = "SELECT no FROM study_group WHERE group_id = '%s'" % (group_id)
			cursor.execute(getgroupnosql)
			group_no = cursor.fetchone()[0]
			
			getjoin_group = "SELECT join_group FROM user WHERE user_id = '%s'" % (join_id)
			cursor.execute(getjoin_group)
			join_g = cursor.fetchone()[0]
			
			joined_data = join_g + str(group_no) +','
			
			updatejoingroupsql = "UPDATE user SET join_group = '%s' WHERE user_id ='%s'" % (joined_data,join_id)
			cursor.execute(updatejoingroupsql)
			
			getgroup_member = "SELECT group_member FROM study_group WHERE group_id = '%s'" % (group_id)
			cursor.execute(getgroup_member)
			g_member = cursor.fetchone()[0]
			
			getuserno = "SELECT no FROM user WHERE user_id = '%s'" % (join_id)
			cursor.execute(getuserno)
			user_no = cursor.fetchone()[0]
			
			joined_member = g_member + str(user_no) +','
			updatejoingroupsql = "UPDATE study_group SET group_member = '%s' WHERE group_id ='%s'" % (joined_member,group_id)
			cursor.execute(updatejoingroupsql)
			
			#update group number
			updatemembernum = "UPDATE study_group SET member_num = member_num+1 WHERE group_id ='%s'" %(group_id)
			cursor.execute(updatemembernum)
			return HttpResponseRedirect('/group/{}'.format(group_id))


def user(request,user_id):
	
	cursor = connection.cursor()
	selectsql = "SELECT join_group FROM user WHERE user_id = '%s'" %(user_id)
	cursor.execute(selectsql)
	user_group = cursor.fetchone()[0][:-1]
	
	getgroupinfosql = "SELECT group_id,group_name,intro,created_time,finished_time FROM study_group WHERE no in ("+user_group+")";
	cursor.execute(getgroupinfosql)
	group_data = cursor.fetchall()
	
	data_list = []
	for x in group_data:
		group = {
			'group_id': x[0],
				'group_name':x[1],
				'intro': x[2],
				'created_time':x[3],
				'finished_time':x[4],
		}
		data_list.append(group)
	return render(request,'user.html',{'user_page_data':data_list})


def group_member_inf(request,group_id):
	
	cursor = connection.cursor()
	getgroup_membersql = "SELECT group_member FROM study_group WHERE group_id ='%s'" % (group_id);
	cursor.execute(getgroup_membersql)
	data = cursor.fetchone()[0][:-1]
	
	group_member_data = data.split(',')
	user_inf = []
	for member in group_member_data:
		getuserinfsql = "SELECT name,email FROM user WHERE no = '%d'" %(int(member))
		cursor.execute(getuserinfsql)
		tmp = cursor.fetchone()
		user_inf.extend(list(tmp))
	return HttpResponse(",".join(user_inf))


def userno(request,user_id):
	
	cursor = connection.cursor()
	getuserno = "SELECT no FROM user WHERE user_id ='%s'" % (user_id);
	cursor.execute(getuserno)
	data = cursor.fetchone()[0]
	return HttpResponse(data)


def getcalendarevent(request,group_id):
	
	cursor = connection.cursor()
	getcalendarsql = "SELECT * FROM calendar WHERE group_id ='%s'" % (group_id);
	cursor.execute(getcalendarsql)
	date = cursor.fetchall()
	returnstr = ''
	for a in date:
		returnstr = returnstr + a[1] +';'
	return HttpResponse(returnstr)


@csrf_exempt
def postcalendarevent(request,group_id):
	
	event = request.POST['title']
	date = request.POST['start']
	event = strcheck(event)
	st = event+ ',' + date
	sql = "INSERT INTO calendar(group_id, event) VALUES('%s','%s')" % (group_id,st)
	cursor = connection.cursor()
	cursor.execute(sql)
	return HttpResponseRedirect('/group/{}'.format(group_id))


@csrf_exempt
def deletecalendarevent(request,group_id):
	
	event = request.POST['title']
	date = request.POST['start']
	content = event + ',' +date
	sql = "DELETE FROM calendar WHERE group_id ='%s' AND event='%s' " % (group_id,content)
	cursor = connection.cursor()
	cursor.execute(sql)
	return HttpResponseRedirect('/group/{}'.format(group_id))


def get_group_news(request,group_id):
	
	cursor = connection.cursor()
	get_group_newssql = "SELECT * FROM news WHERE group_id ='%s' ORDER BY no DESC" % (group_id);
	cursor.execute(get_group_newssql)
	data = cursor.fetchall()
	news_str = ''
	for news in data:
		news_str = news_str + news[2]+',' +news[3] + ',' + news[4] + ';'
	return HttpResponse(news_str)


@csrf_exempt
def post_group_news(request,group_id):
	
	title = request.POST['title']
	content = request.POST['content']
	t = time.time()
	date = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')
	cursor = connection.cursor()
	title = strcheck(title)
	content = strcheck(content)
	print(title)
	print(content)
	post_group_newssql = "INSERT INTO news(group_id,title,content,created_time) VALUES('%s','%s','%s','%s')" % (group_id,title,content,date);
	cursor.execute(post_group_newssql)
	return HttpResponseRedirect('/group/{}'.format(group_id))


def strcheck(string):
	
	if '"' in string:
		a = string.replace('"', '\\\"')
	elif "'"  in string:
		a = string.replace("'", '\\\'')
	elif '\\' in string:
		a = string.replace("'", '\\\\')
	else:
		a = string
	return a
