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
			selectsql = "SELECT * FROM  user WHERE user_id = '%s'" %(creator)
			cursor.execute(selectsql)
			user_data = cursor.fetchone()
			
			if(len(user_data)) > 0:
				user_no = user_data[0]
				str_user_no = str(user_no)+','
				user_join_group = user_data[5]
				
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
				get_user_achievement_sql = "SELECT exp FROM user WHERE no = '%d'" % (user_no)
				cursor.execute(get_user_achievement_sql)
				exp = cursor.fetchone()[0]
				print('ff')

				if 15<=exp+10 <= 49:
					update_user_achievement_sql = "UPDATE  user SET exp = exp + 10 ,level =1, created_achieve=1, join_group = '%s' WHERE no = '%d' " %(user_join_group,user_no)
			
				elif 50<=exp+10 <= 89:
					update_user_achievement_sql = "UPDATE  user SET exp = exp + 10 ,level =2, created_achieve=1, join_group = '%s' WHERE no = '%d' " %(user_join_group,user_no)
			
				elif 90<=exp+10 <= 139:
					update_user_achievement_sql = "UPDATE  user SET exp = exp + 10 ,level =3, created_achieve=1, join_group = '%s' WHERE no = '%d' " %(user_join_group,user_no)
		
				elif 140<=exp+10:
					update_user_achievement_sql = "UPDATE  user SET exp = exp + 10 ,level =4, created_achieve=1, join_group = '%s' WHERE no = '%d' " %(user_join_group,user_no)
			
				else:
					update_user_achievement_sql = "UPDATE  user SET exp = exp + 10 , created_achieve=1, join_group = '%s' WHERE no = '%d' " %(user_join_group,user_no)
		
				cursor.execute(update_user_achievement_sql)
				
				return HttpResponseRedirect('/group/{}'.format(group_id))

			
			else:
				#handle no this user's id in database
				print('hh')

		# login
		elif 'user_email' in request.POST:
			id = request.POST['user_id']
			email = request.POST['user_email']
			name = request.POST['user_name']
			pic = request.POST['user_pic']
			cursor = connection.cursor()
			selectsql = "SELECT * FROM  user WHERE user_id = '%s';" %(id)
			cursor.execute(selectsql)
			user_data = cursor.fetchall()
			cursor2 = connection.cursor()
			if len(user_data) == 0:
				insertsql = "INSERT INTO user(name,user_id,email,login_cnt,pic) VALUES ('%s','%s','%s',1,'%s')" %(name,id,email,pic)
				cursor2.execute(insertsql)
			else:
				updatesql = "UPDATE  user SET login_cnt = login_cnt + 1 WHERE user_id = '%s'" % (id)
				cursor2.execute(updatesql)
			return HttpResponseRedirect("/")

		# store user large picture
		elif 'user_pic_large' in request.POST:
			print('fff')
			id = request.POST['user_id']
			pic_large = request.POST['user_pic_large']
			cursor = connection.cursor()
			
			updatesql = "UPDATE  user SET pic_large = '%s' WHERE user_id = '%s'" % (pic_large,id)
			cursor.execute(updatesql)
			print(pic_large)
			return HttpResponseRedirect("/")
	
	if request.method == 'GET':
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM study_group;")
		group_data = cursor.fetchall()
		data_list = []
		for x in group_data:
			get_user_sql = "SELECT name FROM  user WHERE user_id = '%s'" % x[10]
			cursor.execute(get_user_sql)
			tmp = cursor.fetchone()
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
				'creator': tmp[0]
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
			
			getjoin_group = "SELECT join_group FROM  user WHERE user_id = '%s'" % (join_id)
			cursor.execute(getjoin_group)
			join_g = cursor.fetchone()[0]
			
			joined_data = join_g + str(group_no) +','
			
			updatejoingroupsql = "UPDATE  user SET join_group = '%s' WHERE user_id ='%s'" % (joined_data,join_id)
			cursor.execute(updatejoingroupsql)
			
			getgroup_member = "SELECT group_member FROM study_group WHERE group_id = '%s'" % (group_id)
			cursor.execute(getgroup_member)
			g_member = cursor.fetchone()[0]
			
			getuserno = "SELECT no FROM  user WHERE user_id = '%s'" % (join_id)
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
	selectsql = "SELECT join_group, login_cnt, post_int, created_achieve FROM  user WHERE user_id = '%s'" %(user_id)
	cursor.execute(selectsql)
	data = cursor.fetchone()
	user_group = data[0][:-1]
	user_login_cnt = data[1]
	user_post_int = data[2]
	user_created_achieve = data[3]
	user_achievement = {'user_login_cnt': user_login_cnt, 'user_post_int': user_post_int, 'user_created_achieve': user_created_achieve}
	print(user_achievement)
	if user_group == '':
		return render(request, 'user_page.html', {'user_achievement_data':user_achievement})
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
		return render(request, 'user_page.html', {'user_page_data':data_list, 'user_achievement_data':user_achievement})

def group_member_inf(request,group_id):
	
	cursor = connection.cursor()
	getgroup_membersql = "SELECT group_member FROM study_group WHERE group_id ='%s'" % (group_id);
	cursor.execute(getgroup_membersql)
	data = cursor.fetchone()[0][:-1]

	group_member_data = data.split(',')
	user_inf = ''
	for member in group_member_data:
		getuserinfsql = "SELECT name,email,pic FROM  user WHERE no = '%d'" %(int(member))
		cursor.execute(getuserinfsql)
		tmp = cursor.fetchone()
		
		user_inf = user_inf + tmp[0] + ',' + tmp[1] + ',' + tmp[2] + ';'
	return HttpResponse(user_inf)


def userno(request,user_id):
	
	cursor = connection.cursor()
	getuserno = "SELECT no FROM  user WHERE user_id ='%s'" % (user_id);
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
	
	post_group_newssql = "INSERT INTO news(group_id,title,content,created_time) VALUES('%s','%s','%s','%s')" % (group_id,title,content,date);
	cursor.execute(post_group_newssql)
	return HttpResponseRedirect('/group/{}'.format(group_id))


def get_group_materials(request,group_id):

	cursor = connection.cursor()
	get_group_materialssql = "SELECT * FROM material WHERE group_id ='%s' ORDER BY no DESC" % (group_id);
	cursor.execute(get_group_materialssql)
	data = cursor.fetchall()

	post_content = ''
	if data:
		for material in data:
			get_user_sql = "SELECT name FROM  user WHERE user_id = '%s'" % material[6]
			cursor.execute(get_user_sql)
			data1 = cursor.fetchone()
			if data1:
				post_content += str(material[0]) + ',' + material[3] + ',' + material[4] + ',' + material[5] + ',' + data1[0] + ';'
			else:
				post_content += str(material[0]) + ',' + material[3] + ',' + material[4] + ',' + material[5] + ',0;'

	
	return HttpResponse(post_content)


@csrf_exempt
def post_group_materials(request,group_id):

	title = strcheck(request.POST['title'])
	content = strcheck(request.POST['content'])
	creator_id = request.POST['creator_id']
	t = time.time()
	date = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')
	cursor = connection.cursor()
	post_materials_sql = "INSERT INTO material(group_id, title, content, created_time, creator_id) VALUES('%s','%s','%s','%s','%s')" % (group_id, title, content, date, creator_id)
	cursor.execute(post_materials_sql)

	get_user_achievement_sql = "SELECT exp FROM user WHERE user_id = '%s'" % (creator_id)
	cursor.execute(get_user_achievement_sql)
	exp = cursor.fetchone()[0]
	if 15<=exp+5 <= 49:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5,post_int = post_int +1, level = 1 WHERE user_id = '%s'" % (creator_id)
	elif 50<=exp+5 <= 89:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5,post_int = post_int +1, level = 2 WHERE user_id = '%s'" % (creator_id)
		
	elif 90<=exp+5 <= 139:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5,post_int = post_int +1, level = 3 WHERE user_id = '%s'" % (creator_id)
	elif 140<=exp+5 :
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5,post_int = post_int +1, level = 4 WHERE user_id = '%s'" % (creator_id)
	else:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5 WHERE user_id = '%s'" % (creator_id)
				
			
	cursor.execute(update_user_achievement_sql)
	return HttpResponseRedirect('/group/{}'.format(group_id))

@csrf_exempt
def set_mail_read(request,user_id):
	if request.method == 'POST':
		mail_no = request.POST['mail_no']

		get_unread_mail_sql = "SELECT mail_unread FROM user WHERE user_id ='%s'" % user_id
		cursor = connection.cursor()
		cursor.execute(get_unread_mail_sql)
		data = cursor.fetchone()[0][:-1].split(',')
		newdata = ''
		for d in data:
			if mail_no != d:
				newdata = newdata + d + ','
		

		set_new_unread_sql = "UPDATE user SET mail_unread = '%s' WHERE user_id = '%s'" % (newdata,user_id)
		cursor.execute(set_new_unread_sql)
		return HttpResponse()



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
		insertmailboxsql = "INSERT INTO mailbox(creator_id,title,content,created_time,group_id,checkno) VALUES('%s','%s','%s','%s','%s','%s')" % (creator_id,title,content,created_time,group_id,t)
		cursor.execute(insertmailboxsql)

		get_mail_no = "SELECT no FROM mailbox WHERE checkno = '%s' " % (t)
		cursor.execute(get_mail_no)
		mail_no = cursor.fetchone()[0]

		

		getgroup_member_sql = "SELECT group_member FROM study_group WHERE group_id = '%s'" % (group_id)
		cursor.execute(getgroup_member_sql)
		tmp_member = cursor.fetchone()[0][:-1]
		group_member = tmp_member.split(',')
		for member in group_member:

			get_mail = "SELECT mail,mail_unread FROM user WHERE no ='%d'" %(int(member))
			cursor.execute(get_mail)
			data = cursor.fetchone()

			mail_data = data[0] + str(mail_no) + ','
			mail_unread = data[1] + str(mail_no) + ','

			update_mail_sql = "UPDATE  user SET mail = '%s' WHERE no = '%d' " %(mail_data,int(member))
			cursor.execute(update_mail_sql) 

			update_mail_unread_sql = "UPDATE  user SET mail_unread = '%s' WHERE no = '%d' " %(mail_unread,int(member))
			cursor.execute(update_mail_unread_sql)

		return HttpResponseRedirect('/group/{}'.format(group_id))


def get_mail(request,user_id):

	cursor = connection.cursor()
	get_all_mail_no_sql = "SELECT mail,mail_unread FROM user WHERE user_id = '%s'" %(user_id)

	cursor.execute(get_all_mail_no_sql)
	data = cursor.fetchone()
	print(data)
	unread = data[1][:-1].split(',')
	all_mail_no = data[0][:-1]
	
	split_no = all_mail_no.split(',')
	data = ''
	for no in split_no:
		get_mail_content_sql = "SELECT * FROM mailbox WHERE no = '%d'" %(int(no))
		cursor.execute(get_mail_content_sql)
		if no in unread:
			tag = 'n'
		else:
			tag = 'y'
		
		tmp_data = cursor.fetchone()
		tmp2_data = str(no) + ',' + tmp_data[3]+','+tmp_data[4]+','+tmp_data[5] + ','+ tag + ';';

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

			get_member_name = "SELECT name,mission FROM  user WHERE no = '%d'" % int(member)
			cursor.execute(get_member_name)
			tmp = cursor.fetchone()[0]
			name_list.append(tmp)



		ranint = random.randint(1,100)

		choose_person = ranint % len(name_list)
		get_choosed_member_user_id = "SELECT pic_large FROM  user WHERE name = '%s'" % name_list[choose_person]
		cursor.execute(get_choosed_member_user_id)

		#question_url is the question
		#ans_name is the ans
		question_pic = cursor.fetchone()[0]
		print(question_pic)
		ans_name = name_list[choose_person]
		name_list_string = ''
		for a in name_list:
			name_list_string = name_list_string + a +','


		#get time
		t = time.time()
		created_time = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d-%h%m%s')

		insert_mission_sql = "INSERT INTO mission(question_pic,question_name,ans,time) VALUES ('%s','%s','%s','%s')" % (question_pic,name_list_string,ans_name,t)
		cursor.execute(insert_mission_sql)

		print('ffff' )
		#get mission no
		get_mission = "SELECT no FROM mission WHERE time ='%s'" % t
		cursor.execute(get_mission)
		mission_no = cursor.fetchone()[0]
		#insert mission to user

		for m in member_list:
			#get_user_origin mission first
			get_user_mission = "SELECT mission FROM  user WHERE no ='%d'" % int(m)
			cursor.execute(get_user_mission)
			tmp = cursor.fetchone()[0]

			tmp = tmp + str(mission_no)+ ','
			#update  user mission

			update_user_mission = "UPDATE  user SET mission = '%s' WHERE no ='%d'" % (tmp,int(m))
			cursor.execute(update_user_mission)

	return HttpResponse("hello")


def get_mission(request,user_id):
	print(user_id)
	get_user_mission = "SELECT mission FROM  user WHERE user_id='%s'" % user_id
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

def get_group_thoughts(request, group_id):

	cursor = connection.cursor()
	get_thoughts_sql = "SELECT * FROM thought WHERE group_id ='%s' ORDER BY no DESC" % (group_id)
	cursor.execute(get_thoughts_sql)
	data = cursor.fetchall()
	thought_str = ''
	if data:
		for thought in data:
			get_user_sql = "SELECT name FROM  user WHERE user_id = '%s'" % thought[5]
			cursor.execute(get_user_sql)
			data4 = cursor.fetchone()
			thought_str += str(thought[0]) + ',' + thought[2] + ',' + thought[3] + ',' + thought[4] + ',' + data4[0]
			get_reply_sql = "SELECT * FROM thought_reply WHERE thought_id ='%d' ORDER BY no DESC" % (int(thought[0]))
			cursor.execute(get_reply_sql)
			data2 = cursor.fetchall()

			if data2:
				for i, reply in enumerate(data2):
					get_user_sql = "SELECT name,pic FROM  user WHERE user_id = '%s'" % reply[4]
					cursor.execute(get_user_sql)
					data3 = cursor.fetchone()
					if data3:
						thought_str += ',' + reply[2] + ',' + reply[3] + ',' + data3[0] + ',' + data3[1]
					else:
						thought_str += ',' + reply[2] + ',' + reply[3] + ',0,0'
				thought_str += ';'
			else:
				thought_str += ';'
		
		return HttpResponse(thought_str)
	else:
		return HttpResponse("")


@csrf_exempt
def post_group_thoughts(request, group_id):

	title = strcheck(request.POST['title'])
	content = strcheck(request.POST['content'])
	creator_id = request.POST['creator_id']
	t = time.time()
	date = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')
	cursor = connection.cursor()
	post_thoughts_sql = "INSERT INTO thought(group_id, title, content, created_time, creator_id) VALUES('%s','%s','%s','%s','%s')" % (group_id, title, content, date, creator_id)
	cursor.execute(post_thoughts_sql)

	get_user_achievement_sql = "SELECT exp FROM user WHERE user_id = '%s'" % (creator_id)
	cursor.execute(get_user_achievement_sql)
	exp = cursor.fetchone()[0]
	if 15<=exp+5 <= 49:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5,post_int = post_int +1, level = 1 WHERE user_id = '%s'" % (creator_id)
	elif 50<=exp+5 <= 89:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5,post_int = post_int +1, level = 2 WHERE user_id = '%s'" % (creator_id)
		
	elif 90<=exp+5 <= 139:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5,post_int = post_int +1, level = 3 WHERE user_id = '%s'" % (creator_id)
	elif 140<=exp+5 :
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5,post_int = post_int +1, level = 4 WHERE user_id = '%s'" % (creator_id)
	else:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 5 WHERE user_id = '%s'" % (creator_id)
						
	cursor.execute(update_user_achievement_sql)

	return HttpResponseRedirect('/group/{}'.format(group_id))


@csrf_exempt
def post_group_thought_reply(request, group_id):

	content = strcheck(request.POST['content'])
	thought_id = request.POST['thought_id']
	creator_id = request.POST['creator_id']
	t = time.time()
	date = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')
	cursor = connection.cursor()
	post_reply_sql = "INSERT INTO thought_reply(thought_id,content,created_time, creator_id) VALUES('%s','%s','%s','%s')" % (thought_id, content, date, creator_id);
	cursor.execute(post_reply_sql)
	
	get_user_achievement_sql = "SELECT exp FROM user WHERE user_id = '%s'" % (creator_id)
	cursor.execute(get_user_achievement_sql)
	exp = cursor.fetchone()[0]
	if 15<=exp+1 <= 49:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 1, level = 1 WHERE user_id = '%s'" % (creator_id)
	elif 50<=exp+1 <= 89:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 1, level = 2 WHERE user_id = '%s'" % (creator_id)
	elif 90<=exp+1 <= 139:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 1, level = 3 WHERE user_id = '%s'" % (creator_id)
	elif 140<=exp+1 :
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 1, level = 4 WHERE user_id = '%s'" % (creator_id)
	else:
		update_user_achievement_sql = "UPDATE  user SET exp = exp + 1 WHERE user_id = '%s'" % (creator_id)
						
	cursor.execute(update_user_achievement_sql)

	return HttpResponseRedirect('/group/{}'.format(group_id))


@csrf_exempt
def post_file(requext, group_id):
	return HttpResponseRedirect('/group/{}'.format(group_id))


def get_my_group(request,user_id):
	
	cursor = connection.cursor()
	selectsql = "SELECT join_group FROM  user WHERE user_id = '%s'" %(user_id)
	cursor.execute(selectsql)

	
	user_group = cursor.fetchone()[0][:-1]
	
	if user_group == '':
		return HttpResponse('')
	else:
		getgroupinfosql = "SELECT group_id,group_name,intro,created_time,finished_time,member_limit,member_num,creator FROM study_group WHERE no in ("+user_group+")"
		cursor.execute(getgroupinfosql)
		
		group_data = cursor.fetchall()
		
		data_list = ''
		for x in group_data:
			
			get_user_sql = "SELECT name FROM  user WHERE user_id = '%s'" % x[7]
			cursor.execute(get_user_sql)
			tmp = cursor.fetchone()[0]
			data_list = data_list + str(x[0]) + ',' + str(x[1]) + ',' + str(x[2]) + ',' + str(x[3]) + ',' + str(x[4]) + ',' + str(x[5]) + ',' + str(x[6]) + ',' + tmp+ ';'
			#data_list = data_list + group_data[x][0]
		
		return HttpResponse(data_list)

def check_mail(request,user_id):
	get_unread = "SELECT mail_unread FROM user WHERE user_id = '%s' " % user_id
	cursor = connection.cursor()
	cursor.execute(get_unread)

	data = cursor.fetchone()[0]
	print(data)
	if(len(data) > 0):
		return HttpResponse('y')
	
	else:
		return HttpResponse('n')



@csrf_exempt
def mission_complete(request,user_id):
	mission_no = request.POST['mission_no']
	correct = request.POST['correct']

	get_user_data_sql = "SELECT exp,mission FROM user WHERE user_id = '%s'" % (user_id)
	cursor = connection.cursor()
	cursor.execute(get_user_data_sql)
	data = cursor.fetchone()
	if correct == 1:	# correct answer
		exp = data[0]

		if 15<=exp+1 <= 49:
			update_user_achievement_sql = "UPDATE user SET exp = exp + 5, level = 1 WHERE user_id = '%s'" % (user_id)
		elif 50<=exp+1 <= 89:
			update_user_achievement_sql = "UPDATE user SET exp = exp + 5, level = 2 WHERE user_id = '%s'" % (user_id)
		elif 90<=exp+1 <= 139:
			update_user_achievement_sql = "UPDATE user SET exp = exp + 5, level = 3 WHERE user_id = '%s'" % (user_id)
		elif 140<=exp+1 :
			update_user_achievement_sql = "UPDATE user SET exp = exp + 5, level = 4 WHERE user_id = '%s'" % (user_id)
		else:
			update_user_achievement_sql = "UPDATE user SET exp = exp + 5 WHERE user_id = '%s'" % (user_id)

		cursor.execute(update_user_achievement_sql)

	mission_list = data[1][:-1].split(',')
	if mission_no in mission_list:	# remove completed mission
		mission_list.remove(mission_no)
	print(mission_list)

	new_mission_list = ''
	for mission in mission_list:
		new_mission_list = new_mission_list + mission + ','
	print(new_mission_list)

	update_user_mission_sql = "UPDATE user SET mission = '%s' WHERE user_id = '%s'" % (new_mission_list,user_id)
	cursor.execute(update_user_mission_sql)
	
	return HttpResponse("hello")


def get_user_experience(request,user_id):
	
	cursor = connection.cursor()
	selectsql = "SELECT exp, level FROM  user WHERE user_id = '%s'" %(user_id)
	cursor.execute(selectsql)	
	data = cursor.fetchone()
	exp = data[0]
	level = data[1]
	print('ff')
	data_list = str(level) + ',' + str(exp)
	print(data_list)
	return HttpResponse(data_list)

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
