$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});

function checkShowLoginDiv() {
    user_id = Cookies.get('user_id');
	if(user_id != undefined)
		adjustCSS();
}
/*function closecal(){
    $("#finished_time_date").attr('disabled','disabled');
}

function opencal(){
$("#finished_time_date").removeAttr('disabled');
}
*/
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
    $.post( "/index/", { group_id : group_id, group_name : group_name,  member_limit :member_limit,intro:intro,private:private,creator_id:creator_id ,finished_time:finished_time})
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
	window.location = '/index/';
}

function saveUserInfo() {

	FB.api('/me',{"fields": "name, email"}, function(response) {
		   if(response && !response.error) {

               $.post("/index/",{
                   user_id : response.id, user_name: response.name, user_email: response.email})
                   .then(function(){
						 adjustCSS();
						 Cookies.set('user_id',response.id);
						 console.log('Successful login for: ' + response.name + ' with ' + response.id + ' and ' + response.email);
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
