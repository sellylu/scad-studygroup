$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});

function checkShowLoginDiv() {
    user_id = Cookies.get('user_id');
	if(user_id != undefined) {
		adjustCSS();
    }
}

function creategroup_submit() {
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
	if(check_group_intro =='') {
		$('#introdiv').attr('class','form-group has-error');
		nosubmit =1;
    } else {
		$('#introdiv').attr('class','form-group');
	}
	if(check_group_name=='') {
		$('#namediv').attr('class','form-group has-error');
		nosubmit =1;
    } else {
		$('#namediv').attr('class','form-group');
	}
	if(nosubmit==1)return false;

    creator_id = Cookies.get('user_id');
    group_name = document.getElementById("group_name").value;
    intro = document.getElementById("intro").value;
	finished_time = document.getElementById("datepicker").value;
    if(document.getElementById("private_op1").checked){
        private = 0;
    }else{
        private = 1;
    }
    date = Date.now();
    group_id = creator_id + date;
	member_limit = parseInt(document.getElementsByName("member_limit")[0].value);

    $.post( "/", { group_id : group_id, group_name : group_name,  member_limit :member_limit,intro:intro,private:private,creator_id:creator_id ,finished_time:finished_time})
        .then(function () {
            window.location = '/group/'+group_id;
        });
}

function getMyInfoURL(){
	user_id = Cookies.get('user_id');
	window.location = '/user/'+user_id;
}
function logout(){
	Cookies.remove('user_id');
	window.location = '/';
}

function saveUserInfo() {

	FB.api('/me',{"fields": "name, email, picture","type":"large"}, function(response) {
		   if(response && !response.error) {

               $.post("/",{
                   user_id : response.id, user_name: response.name, user_email: response.email, user_pic: response.picture.data.url})
                   .then(function(){
						 adjustCSS();
						 Cookies.set('user_id',response.id);
                         appendMyGroup();
						 });
            }
		});
}

function adjustCSS() {
	$('body').css('padding-top', '70px');
	$('#about-us').hide();
	$('#navbar-button').show();
	$('#create_group_button').show();
	$('#NavBar').css('background-color', 'black');
	$('a.navbar-brand').css('color', '#dddddd');
}

function appendMyGroup() {
            user_id = Cookies.get('user_id');
            if(user_id != undefined) {
                $('#joined-group').empty();
                user_id = Cookies.get('user_id');
                str = '/get_my_group/' + user_id + '/';

                $.get(str, function(data){
                    var tmp = data.split(";");
                    var groups = '';
                    for(var i = 0; i < tmp.length-1; i++) {
                        tmp2 = tmp[i].split(',');
                        group_id = tmp2[0];
                        group_name = tmp2[1];
                        group_intro = tmp2[2];
                        group_created_time = tmp2[3];
                        group_finished_time = tmp2[4];
                        member_limit = tmp2[5];
                        member_num = tmp2[6];
                        creator = tmp2[7];

                        if(member_limit == 0) {
                            groups += '<div class="col-md-4"><div class="panel panel-warning"><div class="panel-heading"><a href="/group/' + group_id + '/"><div><h4 align="center">' + group_name + '</h4></div></a></div><div class="panel-body"><p align="center">' + group_intro + '</p><hr><p><b>Period:</b>' + group_created_time + '~' + group_finished_time + '<br><b>Number of Members and Limitation:</b> ' + member_num + ' / ∞<br><b>Creator:</b>' + creator + '</p></div></div></div>';
                        }
                        else {
                            groups += '<div class="col-md-4"><div class="panel panel-warning"><div class="panel-heading"><a href="/group/' + group_id + '/"><div><h4 align="center">' + group_name + '</h4></div></a></div><div class="panel-body"><p align="center">' + group_intro + '</p><hr><p><b>Period:</b>' + group_created_time + '~' + group_finished_time + '<br><b>Number of Members and Limitation:</b> ' + member_num + ' / ' + member_limit + '<br><b>Creator:</b>' + creator + '</p></div></div></div>';
                        }
                    }

            
                    $('#joined-group').append('<div class="col-md-12"><h2>My Groups</h2><br class="space"></div><hr style="height:2px; background-color:#d4d4d4;">');
                    $('#joined-group').append(groups);
                    console.log(data);
                });  

                
                check_mail_init(user_id);
            }           
}

(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "//connect.facebook.net/en_US/sdk.js";
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

    
