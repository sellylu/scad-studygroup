from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import time
import datetime
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
import random

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
			pic = request.POST['user_pic']
			cursor = connection.cursor()
			selectsql = "SELECT * FROM user WHERE user_id = '%s';" %(id)
			cursor.execute(selectsql)
			user_data = cursor.fetchall()
			cursor2 = connection.cursor()
			if len(user_data) == 0:
				insertsql = "INSERT INTO user(name,user_id,email,login_cnt,pic) VALUES ('%s','%s','%s',1,'%s')" %(name,id,email,pic)
				cursor2.execute(insertsql)
			else:
				updatesql = "UPDATE user SET login_cnt = login_cnt + 1 WHERE user_id = '%s'" % (id)
				cursor2.execute(updatesql)
			return HttpResponseRedirect("/")
	
	if request.method == 'GET':
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM study_group;")
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
			return render(request, 'group_page.html', {'group_page_data':group})
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
	
	if user_group == '':
		return render(request, 'user_page.html')
	else:
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
		return render(request, 'user_page.html', {'user_page_data':data_list})


def group_member_inf(request,group_id):
	
	cursor = connection.cursor()
	getgroup_membersql = "SELECT group_member FROM study_group WHERE group_id ='%s'" % (group_id);
	cursor.execute(getgroup_membersql)
	data = cursor.fetchone()[0][:-1]

	group_member_data = data.split(',')
	user_inf = ''
	for member in group_member_data:
		getuserinfsql = "SELECT name,email,pic FROM user WHERE no = '%d'" %(int(member))
		cursor.execute(getuserinfsql)
		tmp = cursor.fetchone()
		user_inf = user_inf + tmp[0] + ',' + tmp[1] + ',' + tmp[2] + ';'
	return HttpResponse(user_inf)


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


def get_group_materials(request,group_id):

	cursor = connection.cursor()
	get_group_materialssql = "SELECT * FROM material WHERE group_id ='%s' ORDER BY no DESC" % (group_id);
	cursor.execute(get_group_materialssql)
	data = cursor.fetchall()

	post_content = ''
	for content in data:
		post_content = content[1] + content[2]+',' +content[3] + ',' + content[4] + ';'

	return HttpResponse(post_content)


@csrf_exempt
def post_group_materials(request,group_id):

	title = request.POST['title']
	content = request.POST['content']
	t = time.time()
	date = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')
	cursor = connection.cursor()

	title = strcheck(title)
	content = strcheck(content)

	post_group_materialsql = "INSERT INTO material(group_id,title,content,created_time) VALUES('%s','%s','%s','%s')" % (group_id,title,content,date);
	cursor.execute(post_group_materialsql)

	return HttpResponseRedirect('/group/{}'.format(group_id))

@csrf_exempt
def send_mail(request,group_id):
	if request.method == 'POST':

		creator_id = request.POST['creator_id']

		title = request.POST['title']
		content = request.POST['content']
		title = strcheck(title)
		content = strcheck(content)

		t = time.time()
		created_time = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')

		cursor = connection.cursor()
		insertmailboxsql = "INSERT INTO mailbox(creator_id,title,content,created_time,group_id) VALUES('%s','%s','%s','%s','%s')" % (creator_id,title,content,created_time,group_id)
		cursor.execute(insertmailboxsql)

		get_mail_no = "SELECT no FROM mailbox WHERE group_id = '%s' " % (group_id)
		cursor.execute(get_mail_no)
		mail_no = cursor.fetchall()

		no_str = ''
		for no in mail_no:
			no_str = no_str + str(no[0])+ ','

		getgroup_member_sql = "SELECT group_member FROM study_group WHERE group_id = '%s'" % (group_id)
		cursor.execute(getgroup_member_sql)
		tmp_member = cursor.fetchone()[0][:-1]
		group_member = tmp_member.split(',')

		for member in group_member:
			update_mail_sql = "UPDATE user SET mail = '%s' WHERE no = '%d' " %(no_str,int(member))
			cursor.execute(update_mail_sql)
		return HttpResponseRedirect('/group/{}'.format(group_id))


def get_mail(request,user_id):

	cursor = connection.cursor()
	get_all_mail_no_sql = "SELECT mail FROM user WHERE user_id = '%s'" %(user_id)

	cursor.execute(get_all_mail_no_sql)
	all_mail_no = cursor.fetchone()[0][:-1]
	split_no = all_mail_no.split(',')
	data = ''
	for no in split_no:
		get_mail_content_sql = "SELECT * FROM mailbox WHERE no = '%d'" %(int(no))
		cursor.execute(get_mail_content_sql)

		tmp_data = cursor.fetchone()
		tmp2_data = tmp_data[3]+','+tmp_data[4]+','+tmp_data[5] +';'

		data = data + tmp2_data
	return HttpResponse(data)


@csrf_exempt
def post_mission(request):
	get_group_no_mem = "SELECT no,group_member FROM study_group"
	cursor = connection.cursor()
	cursor.execute(get_group_no_mem)

	group_no_mem = cursor.fetchall()
	group_no_mem_len = len(group_no_mem)

	if group_no_mem_len > 0:
		ranint = random.randint(1,100)
		ranint = ranint % group_no_mem_len
		
		member_list_str = group_no_mem[ranint][1][:-1]
		

		
		member_list = member_list_str.split(',')
		

		name_list = []
		# name_list is question
		for member in member_list:
			
			get_member_name = "SELECT name,mission FROM user WHERE no = '%d'" % int(member)
			cursor.execute(get_member_name)
			tmp = cursor.fetchone()[0]
			name_list.append(tmp)
			
			


		

		ranint = random.randint(1,100)
		
		choose_person = ranint % len(name_list)
		get_choosed_member_user_id = "SELECT user_id FROM user WHERE name = '%s'" % name_list[choose_person]
		cursor.execute(get_choosed_member_user_id)
		
		#question_url is the question
		#ans_name is the ans
		question_user_id = cursor.fetchone()[0]
		ans_name = name_list[choose_person]
		name_list_string = ''
		for a in name_list:
			name_list_string = name_list_string + a +','


		#get time
		t = time.time()
		created_time = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d-%h%m%s')
		
		insert_mission_sql = "INSERT INTO mission(question_user_id,question_name,ans,time) VALUES ('%s','%s','%s','%s')" % (question_user_id,name_list_string,ans_name,t)
		cursor.execute(insert_mission_sql)

		#get mission no
		get_mission = "SELECT no FROM mission WHERE time ='%s'" % t
		cursor.execute(get_mission)
		mission_no = cursor.fetchone()[0]
	
		#insert mission to user

		for m in member_list:
			#get_user_origin mission first
			get_user_mission = "SELECT mission FROM user WHERE no ='%d'" % int(m)
			cursor.execute(get_user_mission)
			tmp = cursor.fetchone()[0]

			tmp = tmp + str(mission_no)+ ','
			#update user mission

			update_user_mission = "UPDATE user SET mission = '%s' WHERE no ='%d'" % (tmp,int(m))
			cursor.execute(update_user_mission)



		return HttpResponse("hello")
def get_mission(request,user_id):

	
	get_user_mission = "SELECT mission FROM user WHERE user_id='%s'" % user_id
	cursor = connection.cursor()
	cursor.execute(get_user_mission)
	mission_str = cursor.fetchone()[0][:-1]
	print(mission_str)
	return HttpResponse(mission_str)
	

def check_Name(request,mission_no):

	get_Mission = "SELECT * FROM mission WHERE no = '%d' " % int(mission_no)
	cursor = connection.cursor()
	cursor.execute(get_Mission)
	data = cursor.fetchone()
	data_str = data[2] +';'+data[3]+';'+data[4]

	return HttpResponse(data_str)

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
