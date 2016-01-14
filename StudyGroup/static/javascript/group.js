$.ajaxSetup({
			data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
			});

var user_id = Cookies.get('user_id');
var member = 0;
var admin = 0;


function checkShowLoginDiv() {
	if(user_id != undefined){
		adjustCSS();
	}
}

function adjustCSS() {
	$('#navbar-button').show();
	$('#create_group_button').show();
	$('#navbar-login').hide();
}

function checkMember() {
	if(member)
		$('.member-btn').show();
	else
		$('.member-btn').hide();
	if(admin)
		$('.admin-btn').show();
	else
		$('.admin-btn').hide();
}

function getMyInfoURL(){
	window.location = '/user/'+user_id+'/';
}

function logout() {
	Cookies.remove('user_id');
	window.location = '/';
}

function send_mail_submit(group_id) {
	check_title = $('#title').val();
	check_content = $("#content").val();

	nosubmit = 0;
	if(check_content =='') {
		$('#mailcontentdiv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#mailcontentdiv').attr('class','form-group');
	}
	if(check_title=='') {
		$('#mailtitlediv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#mailtitlediv').attr('class','form-group');
	}
	if(nosubmit==1)return false;

	title = document.getElementById("title").value;
	content = $("#content").val();

	str = '/send_mail/' + group_id + '/';
	$.post( str, { title : title,  content : content, creator_id: user_id})
		.then(function () {
			setTimeout(function() {
				window.location = '/group/'+group_id;
			}, 3000);
		});
}

// Progress
function showprogress(created_time,finish_time){
	
	var ct = new Date(created_time);
	var ft = new Date(finish_time);
	var nt = new Date();
	
	var alltime = ((ft - ct) / (1000 * 60 * 60 * 24));
	var passtime = Math.floor(((nt - ct) / (1000 * 60 * 60 * 24)));
	
	// limit has pass
	if(alltime ==0 ){
	
		$('progress-bar').attr('style','width:100%');
	}else{
		
		perc = passtime / alltime * 100;
		str = 'width:' + perc + '%';
		$('#progress-bar').attr('style',str);
	}
}

// Create Group

function creategroup_submit() {

	date = Date.now();
    check_group_name = $('#group_name').val();
    check_group_intro = $('#intro').val();
	check_time = $('#datepicker').val();
    nosubmit = 0;
	if(check_time == '') {
		$('#datepicker').attr('style','border: 1px solid red');
		nosubmit =1;
	} else {
		$('#datepicker').removeAttr('style');
	}
	var check = new Date(check_time);
	if(check.valueOf() - date < 0){
		$('#datepicker').attr('style','border: 1px solid red');
		nosubmit =1;
	} else {
		$('#datepicker').removeAttr('style');
	}

	if(check_group_intro =='') {
		$('#introdiv').attr('class','form-group has-error');
		nosubmit =1;
    } else {
		$('#introdiv').attr('class','form-group');
	}
	if(check_group_name=='') {
		$('#creatednamediv').attr('class','form-group has-error');
		nosubmit =1;
    } else {
		$('#creatednamediv').attr('class','form-group');
	}
	if(nosubmit==1)return false;

	group_name = document.getElementById("group_name").value;
	content = $('#intro').val();
	finished_time = document.getElementById("datepicker").value;
	if(document.getElementById("private_op1").checked) {
		private = 0;
	} else {
		private = 1;
	}
	var group_id = user_id + date;
	member_limit = parseInt(document.getElementsByName("member_limit")[0].value);
	
	$.post( "/", { group_id : group_id, group_name : group_name,  member_limit :member_limit,intro:content,private:private,creator_id:user_id ,finished_time:finished_time})
	.then(function () {
		  window.location = '/group/' + group_id;
		  });
	// TODO: display link of the group
}

// News Tab
function showNews(group_id) {

	
	$('#myContent').empty();
	$('#myContent').append('<button type="button" class="btn btn-primary admin-btn" id="add_news_button" data-toggle="modal" data-target="#add_news_Modal">Add News</button>');
	var str = '/get_group_news/' + group_id;
	
	$.get(str, function(data){
		var tmp = data.split(";");
		var news = '';
		for(var i = 0; i < tmp.length-1; i++) {
			tmp2 = tmp[i].split(',');
		    news_date = tmp2[0];
		    news_title = tmp2[1];
		    news_content = tmp2[2];
		    news += '<tr onclick="displayContent(' + i + ')"><td>' + news_date + '</td><td>' + news_title + '</td></tr>' + '<tr class="news_content" id=' + i + '><td colspan="2">' + news_content + '</td></tr>';
		}
		  
		$('#myContent').append('<table class="table table-striped table-hover"><thead><tr><td>DATE</td><td>CONTENT</td></tr></thead><tbody>' + news + '</tbody></table>');
		console.log(data);
		checkMember();
	});
}

function add_group_news(group_id) {
	check_news_title = $('#news_title').val();
	check_news_content = $('#news_content').val();
	
	nosubmit = 0;
	
	if(check_news_content =='') {
		$('#newscontentdiv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#newscontentdiv').attr('class','form-group');
	}
	if(check_news_title=='') {
		$('#newsnamediv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#newsnamediv').attr('class','form-group');
	}
	if(nosubmit==1)return false;
	
	title = document.getElementById("news_title").value;
	content = document.getElementById("news_content").value;
	
	url = '/post_group_news/' + group_id +'/';
	$.post( url, {title : title, content: content})
	.then(function () {
		  window.location = '/group/'+group_id;
		  });
}

function displayContent(id) {
	if(document.getElementById(id).style.display == "none") {
		
		$('#'+id).show();
	}
	else {
		document.getElementById(id).style.display = "none";
	}
}

// Schedule Tab
function showSchedule(group_id) {
	$('#myContent').empty();
	
	var calendarurl = '/group/' + group_id + '/calendar';
	var div = $('<div/>', {id: 'calendar'});
	
	$('#myContent').append(div);
	$('#calendar').fullCalendar({
								// put your options and callbacks here
								events: function( start, end, callback ) {
								$.get(calendarurl, function(data){
									  
									  
									  tmp = data.split(';');
									  for(var i=0;i<tmp.length-1;i++){
									  tmp2 = tmp[i].split(',');
									  event_title = tmp2[0];
									  event_start = tmp2[1];
									  myevent = {title: event_title,start: event_start,allDay:true};
									  $('#calendar').fullCalendar( 'renderEvent', myevent);
									  }
									  });
								
								},
								
								eventClick: function(calEvent, jsEvent, view) {



								

								if(member){
								var c = confirm('Delete it?');
								if(c==true){
								
								title = calEvent.title;
								
								var d = new Date(calEvent.start);
								var year = d.getFullYear();
								var month = (d.getMonth()+1);
								var date = d.getDate();
								if(month<10) month='0'+month;
								if(date<10)date='0'+date;
								var datetime = year + '-' + month + '-' + date;
								
								
								url = '/deletecalendarevent/' + group_id +'/';
		     	$.post(url, { title:title,start: datetime}).then(function(){
								showSchedule(group_id);
				});
								
								
								}
								}
								},
								
								dayClick: function(date, allDay, jsEvent, view) {
									
								
									if (member) {
										var d = new Date(date);
										Cookies.set('dayClickTime', d);
										$("#schedule_addevent_Modal").modal();
						
									}
								}
				
	});
	
}




function add_schedule_event(group_id) {
	check_schedule_content = $("#schedule_content").val();

	nosubmit = 0;

	if(check_schedule_content =='') {
		$('#schedulecontentdiv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#schedulecontentdiv').attr('class','form-group');
	}
	if(nosubmit==1)return false;

	content = $("#schedule_content").val();
	var d = new Date(Cookies.get('dayClickTime'));
	var year = d.getFullYear();
	var month = (d.getMonth() + 1);
	var date = d.getDate();
	if (month < 10) month = '0' + month;
	if (date < 10)date = '0' + date;
	var datetime = year + '-' + month + '-' + date;
	
	var url = '/postcalendarevent/' + group_id + '/';
	$.post(url, {title: content, start: datetime}).
		then(function () {

		$('#schedule_addevent_Modal').modal('hide');
		showSchedule(group_id);
	});
}




// Material Tab
function showMaterials(group_id) {
	$('#myContent').empty();
	var n = new nicEditor({fullPanel: true}).panelInstance('materials_content');

	var newMaterial_str = '<button class="btn btn-success member-btn" id="add_materials_button" data-toggle="modal" data-target="#add_materials_Modal" style="width: auto"><i class="glyphicon glyphicon-plus"/>Add Material</button><br class="space">';
	var output = newMaterial_str + '<div class="panel-group">';

	$.get('/get_group_materials/' + group_id + '/', function(data) {

		data = data.split(";");
		for (var i = 0; i < data.length - 1; i++) {
			tmp = data[i].split(',');
			var material = {
				'no': tmp[0],
				'date': tmp[1],
				'title': tmp[3],
				'content': tmp[2],
				'creator': tmp[4]
			};
			output += '<div class="panel panel-success thought"><div class="panel-heading"><h4><a href="#m' + material.no + '" data-toggle="collapse">'
				+ material.title + '</a></h4><div class="thought-info row"><div class="col-md-8" align="left">Created at: ' + material.date + ' by ' + material.creator + '</div></div></div>'
				+ '<div class="panel-collapse collapse" id="m' + material.no + '">';
			output += '<div class="panel-body">' + material.content + '</div></div></div>';
		}
		output += '</div>';
		$('#myContent').append(output);
		console.log(data);
		checkMember();
	});


}

function add_materials(group_id) {
	check_materials_title = $('#materials_title').val();
	check_materials_content = nic.findEditor("materials_content").getContent();;

	nosubmit = 0;

	if(check_materials_content =='') {
		$('#materialscontentdiv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#materialscontentdiv').attr('class','form-group');
	}
	if(check_materials_title=='') {
		$('#materialsnamediv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#materialsnamediv').attr('class','form-group');
	}
	if(nosubmit==1)return false;

	title = document.getElementById("materials_title").value;
	content = nic.findEditor("materials_content").getContent();

	url = '/post_group_materials/' + group_id +'/';
	$.post( url, {title : title, content: content, creator_id: user_id})
		.then(function () {
			
			$('#add_materials_Modal').modal('hide');
			showMaterials(group_id);
	});
}

// Thought Tab
function showThoughts(group_id,replied) {
	$('#myContent').empty();
	var n = new nicEditor({fullPanel: true}).panelInstance('thought_content');
	$('#thought_content').val('');

	var newThought_str = '<button class="btn btn-success member-btn" data-toggle="modal" data-target="#new_thoughts_Modal" style="width: auto"><i class="glyphicon glyphicon-plus"/>New Thought</button><br class="space">';

	var output = newThought_str + '<div class="panel-group">';

	$.get('/get_group_thoughts/' + group_id + '/', function(data) {
		data = data.split(";");
		var tmp_str = '<ul class="list-group">';
		for (var i = 0; i < data.length - 1; i++) {
			tmp = data[i].split(',');
			var thought = {
				'no': tmp[0],
				'date': tmp[1],
				'title': tmp[2],
				'content': tmp[3],
				'creator': tmp[4]
			};
			reply_num = (tmp.length - 5)/4;
			if(replied == thought.no){
				output += '<div class="panel panel-success thought"><div class="panel-heading"><h4><a href="#t' + thought.no + '" data-toggle="collapse">'
				+ thought.title + '</a></h4><div class="thought-info row"><div class="col-md-8" align="left">Created at: ' + thought.date + ' by ' + thought.creator + '</div><div class="col-md-4" align="right">Replied by ' + reply_num + ' people.</div></div></div>'
				+ '<div class="panel-collapse collapse in" id="t' + thought.no + '">';
			}else{
				output += '<div class="panel panel-success thought"><div class="panel-heading"><h4><a href="#t' + thought.no + '" data-toggle="collapse">'
				+ thought.title + '</a></h4><div class="thought-info row"><div class="col-md-8" align="left">Created at: ' + thought.date + ' by ' + thought.creator + '</div><div class="col-md-4" align="right">Replied by ' + reply_num + ' people.</div></div></div>'
				+ '<div class="panel-collapse collapse" id="t' + thought.no + '">';
			
			}
			output += '<div class="panel-body">' + thought.content + '</div>';
			for (var j = 5; j < tmp.length; j += 4) {
				var obj = {
					'date': tmp[j],
					'content': tmp[j + 1],
					'creator': tmp[j + 2],
					'creator_pic': tmp[j + 3]
				};
				tmp_str += '<li class="list-group-item"><div class="row"><div class="col-md-1"><img src="' + obj.creator_pic + '" class="img-thumbnail"></div>'
					+ '<div class="col-md-11"><div class="reply-info">' + obj.creator + ' / ' + obj.date + '</div>'
					+ '<div class="reply-content">' + obj.content + '</div></div></div></li>';
			}
			output += tmp_str + '</ul><div class="panel-footer"><button class="btn btn-default" id="b' + thought.no + '" onclick="showEditor(' + thought.no + ');">Reply</button><div id="e' + thought.no + '" style="display: none;"><textarea id="ta' + thought.no + '" style="width: 800px; height: 100px;"></textarea><br><button class="btn btn-success" onclick="postReply(\'' + group_id + '\', ' + thought.no + ');">Submit</button></div></div></div></div>';
		}
		output += '</div>';
		$('#myContent').append(output);
		checkMember();
	});
}

function showEditor(thought_id){
	tID = 'ta' + thought_id;
	new nicEditor({fullPanel : true}).panelInstance(tID);
	$('#e'+thought_id).show();
	$('#b'+thought_id).hide();
}

function postReply(group_id, thought_id) {
	tID = 'ta' + thought_id;

	check_thought_content = nic.findEditor(tID).getContent();;

	nosubmit = 0;

	if(check_thought_content =='') {
		$(tID).attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$(tID).attr('class','form-group');
	}
	if(nosubmit==1)return false;

	content = nic.findEditor(tID).getContent();
	$('#e'+thought_id).hide();
	$('#b'+thought_id).show();

	url = '/post_group_thought_reply/' + group_id +'/';

	$.post(url, {content: content, thought_id: thought_id, creator_id: user_id})
		.then(function () {
			showThoughts(group_id,thought_id);
	});
}

function postThought(group_id) {


	check_thought_title = $('#thought_title').val();
	check_thought_content = nic.findEditor("thought_content").getContent();;

	nosubmit = 0;

	if(check_thought_content =='') {
		$('#thoughtcontentdiv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#thoughtcontentdiv').attr('class','form-group');
	}

	if(check_thought_title=='') {
		$('#thoughtnamediv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#thoughtnamediv').attr('class','form-group');
	}
	if(nosubmit==1)return false;

	title = document.getElementById("thought_title").value;
	content = nic.findEditor("thought_content").getContent();


	url = '/post_group_thoughts/' + group_id +'/';

	$.post(url, {title: title, content: content, creator_id: user_id})
		.then(function () {
			
			$('#new_thoughts_Modal').modal('hide');
			showThoughts(group_id,-1);
	});
}

// Member Tab
function Group_Member_inf(id){
	if(member) {
		$('#myContent').empty();
		var str = '/group/' + id + '/member_inf';
		$.get(str, function (data) {
			console.log(data);
			var tmp = data.split(";");
			var member = '';
			for (var i = 0; i < tmp.length - 1; i++) {
				tmp2 = tmp[i].split(',');
				img = '<img src="' + tmp2[2] + '"/>';
				member += '<tr><td>' + tmp2[0] + '</td><td>' + tmp2[1] + '</td><td>' + img + '</td></tr>';
			}
			$('#myContent').append('<table class="table table-striped table-hover"><thead><tr><td>NAME</td><td>EMAIL</td><td>PHOTO</td></tr></thead><tbody>' + member + '</tbody></table>');
			console.log(data);
		});
	} else {
		alert('Please join the group first!');
	}
}

function joinGroup(group_id) {
	// TODO: implement the action for user to join the displayed group
	var str = '/group/' + group_id +'/';
	$.post( str, { group_id : group_id, join_id: user_id })
	.then(function () {
		  $('#join_group_btn').hide();
		  window.location = '/group/'+group_id;
		  });
}

function setuser_no(){
	if(user_id != undefined){
		str = '/userno/' + user_id;
		$.get(str,function(data){
			  Cookies.set('user_no',data);
		});
		check_mail_init(user_id);
	}
}

function saveUserInfo() {
	FB.api('/me',{"fields": "name, email"}, function(response) {
		   if(response && !response.error) {
		   $.post("/",{
				  user_id : response.id, user_name: response.name, user_email: response.email})
		   .then(function(){
					adjustCSS();
					Cookies.set('user_id',response.id);
					console.log('Successful login for: ' + response.name + ' with ' + response.id + ' and ' + response.email);
				 });
		   }
		   });
}

// Facebook
(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "http://connect.facebook.net/en_US/sdk.js";
 fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

function checkLoginState() {
	FB.getLoginStatus(function(response) {
					  statusChangeCallback(response);
					  });
}

function statusChangeCallback(response) {
	if (response.status === 'connected') {
		saveUserInfo();
	} else if (response.status === 'not_authorized') {
		FB.login(function(response) {
				 if (response.authResponse) {
				 FB.api('/me', function (response) {
						saveUserInfo();
						});
				 }
				 }, {scope: 'email'});
	} else {
		alert('Please log ' + 'into Facebook.')
		FB.login(function(response) {
				 if (response.authResponse) {
				 FB.api('/me', function(response) {
						saveUserInfo();
						});
				 }
				 }, {scope: 'email'});
	}
}

window.fbAsyncInit = function() {
	FB.init({
			appId      : '444916912380076',
			cookie     : true,
			xfbml      : true,
			version    : 'v2.5'
			});
};



var show_mail_button_interval;
var start = 0;
function check_mail_init(user_id){
    

    self.setInterval('check_mail(user_id)',5000); 
    //check_mail(user_id);
  
}
function check_mail(user_id){
    url = '/check_mail/' + user_id + '/'
    $.get(url,function(data){
    	if(data == 'y'){
        	// alert('y');
        	if(start ==0){
        		$('#show_mail_button').show();
            	show_mail_button_interval = setInterval(flicker,3000);
            	start =1;
        	}
        }
        else{
        	// alert('n');
        	start = 0;
        	$('#show_mail_button').hide();
            clearInterval(show_mail_button_interval);
            // alert('clear');
        } 
        
        });
    
}
function flicker(){//閃爍函數
        $('#show_mail_button').fadeOut(750).fadeIn(750);
}

