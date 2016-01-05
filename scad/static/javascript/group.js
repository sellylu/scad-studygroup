function adjustCSS() {
	$('#navbar-button').show();
	$('#create_group_button').show();
	$('#navbar-login').hide();
}

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

// News Tab
function showNews(group_id) {
	$('#myContent').empty();

        $('#myContent').append('<button type="button" class="btn btn-primary" id="add_news_button" data-toggle="modal" data-target="#add_news_Modal">Add News</button>');
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
	});
}

function add_group_news(group_id) {
	check_news_title = $('#news_title').val();
	check_news_content = $('#news_content').val();
	
	nosubmit = 0;
	
	if(check_news_content =='') {
		$('#contentdiv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#contentdiv').attr('class','form-group');
	}
	if(check_news_title=='') {
		$('#namediv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#namediv').attr('class','form-group');
	}
	if(nosubmit==1)return false;

	//creator_id = Cookies.get('user_id');
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
		},
		
		dayClick: function(date, allDay, jsEvent, view) {
		    var title = prompt('Add new event');
		   	if(title!=null){
			    var d = new Date(date);
			    var year = d.getFullYear();
			    var month = (d.getMonth()+1);
			    var date = d.getDate();
			    if(month<10) month='0'+month;
			    if(date<10)date='0'+date;
			    var datetime = year + '-' + month + '-' + date;
			   
			    url = '/postcalendarevent/' + group_id +'/';
			    $.post(url, { title:title,start: datetime}).
					then(function(){
						showSchedule(group_id);
				});
			}
		}	    
	});

}

// Thought Tab
function showThoughts() {
	$('#myContent').empty();
	var textarea = $('<textarea/>', {id: 'editor'});
	var div= $('<div/>', {id: 'test'});
	$('#myContent').append(textarea);
	$('#myContent').append(div);
	$('#myContent').append("<button onclick='show()'>Sub</button>");
	$('#editor').jqte();
}

function show() {
	$('#test').html($('#editor').val());
}

// Member Tab
function Group_Member_inf(id){
	$('#myContent').empty();
	var str = '/group/' + id + '/member_inf';
	$.get(str, function(data){
		var tmp = data.split(",");
		var member = '';
		for(var i = 0; i < tmp.length; i+=2) {
			member += '<tr><td>' + tmp[i] + '</td><td>' + tmp[i+1] + '</td></tr>';
		}
		$('#myContent').append('<table class="table table-striped table-hover"><thead><tr><td>NAME</td><td>EMAIL</td></tr></thead><tbody>' + member + '</tbody></table>');
		console.log(data);
	});
}

function joinGroup(group_id) {
	// TODO: implement the action for user to join the displayed group
	var str = '/group/' + group_id +'/';
	join_id = Cookies.get('user_id');
	$.post( str, { group_id : group_id, join_id:join_id })
		.then(function () {
			$('#join_group_btn').hide();
			window.location = '/group/'+group_id;
		});
}

function setuser_no(){
    id = Cookies.get('user_id');
    if(id != undefined){
        str = '/userno/'+id;
        $.get(str,function(data){
            Cookies.set('user_no',data);
        });
    }
}

function checkShowAddButton(member){
	id = Cookies.get('user_id');
    if(id != undefined){

    	user_no = Cookies.get('user_no');
    	showbutton = 0;
		if(user_no != undefined){
			var tmp = member.split(',');
			showbutton = 1;
			for(i=0;i<tmp.length;i++){
				if(user_no == tmp[i]){
					showbutton = 0;
				}
			}
		}

		if(showbutton == 1){
			document.getElementById('join_group_btn').style.visibility = 'visible';
		}else{
			document.getElementById('join_group_btn').style.visibility = 'hidden';
		}

    }else{
    	document.getElementById('join_group_btn').style.visibility = 'hidden';

    }
}
