$.ajaxSetup({
			data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});        	
var ans;

		function creategroup_submit() {
    			check_group_name = $('#group_name').val();
			    check_group_intro = $('#intro').val();
	            check_time = $('#finished_time_date').val();
	            nosubmit = 0;
	            if(check_time == '') {
		            $('#finished_time_date').attr('style','border: 1px solid red');
		            nosubmit =1;
	            } else {
		            $('#finished_time_date').removeAttr('style');
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
	            finished_time = document.getElementById("finished_time_date").value;

	            if(document.getElementById("private_op1").checked) {
		            private = 0;
	            } else {
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
            function logout() {
	            Cookies.remove('user_id');
	            window.location = '/';
            }
            

            function showMission() {
	            $('#myContent').empty();

	            user_id = Cookies.get('user_id');
	            str = '/get_mission/' + user_id + '/';
				$.get(str, function(data){

					mission_list = data.split(',');
					if(mission_list != ''){
						var mission ='';
						for(var i = 0; i < mission_list.length; i++) {
							mission_no = mission_list[i];
							mission = '<div id="' + mission_no + '"><a class="missionBox" href="#name_checking_div" onclick="renderMission(' + mission_no + ')"><div class="list-group-item row"><h4 align="center">Mission from System</h4></div></a></div>';
						}

						$('#myContent').append(mission);
					}
					console.log(data);

				});
            }

			function renderMission(mission_no) {
				
				$("#name_checking_div").empty();
					
				str = '/check_Name/' + mission_no.toString()+ '/';
				
				$.get(str, function(data){

					tmp = data.split(';');
					user_id = tmp[0];

					user_pic = 'http://graph.facebook.com/' + user_id + '/picture?type=large';
		            img = $('<img/>', {
		                'class': 'achievement',
		                src: user_pic,
		                width: 200
		            });
					
					name_list = tmp[1].split(',');
					name = '';
		            for(i = 0; i < name_list.length-1; i++) {
		            	name += '<button type="button" onclick="checkAns(\'' + name_list[i] + '\',' + mission_no + ')">' + name_list[i] + '</button>'; }
		            
					ans = tmp[2];


		        }).then(function () {
		            div = $('<div/>', {
		                'class': 'nameChecking'
		            }).css({
		            	'text-align': 'center'
		            }).html('<p id="question">Who is this?</p><p>' + name +'</p>').prepend(img);

		            $('#name_checking_div').append(div);
		        });
			}

			function checkAns (input, mission_no) {
				if(input == ans) {
					alert('you got it right');
					correct = 1;
				}
				else {
					alert('wrong answerQQ');
					correct = 0;
				}

				user_id = Cookies.get('user_id');
 	            str = '/mission_complete/' + user_id + '/';					
				$.post(str, {user_id: user_id, mission_no: mission_no, correct: correct});								
				parent.$.fancybox.close();	
				$('#'+mission_no).remove();
			}


            function showMailbox() {
	            $('#myContent').empty();

	            user_id = Cookies.get('user_id');
	            str = '/get_mail/' + user_id + '/';

				$.get(str, function(data){
					var tmp = data.split(";");
					var news = '';
					for(var i = 0; i < tmp.length-1; i++) {
						tmp2 = tmp[i].split(',');
						mail_no = tmp2[0];
						mail_title = tmp2[1];
						mail_content = tmp2[2];
						mail_created_time = tmp2[3];
						mail_read = tmp2[4];

						if(mail_read == 'y') {
 							news += '<tr class="mail_read" id="mail_' + mail_no + 'onclick="displayContent(' + mail_no + ')"><td width="10px"></td><td width="200px">' + mail_created_time + '</td><td>' + mail_title + '</td></tr>' + '<tr style="display:none;" id=' + mail_no + '><td colspan="2">' + mail_content + '</td></tr>';
 						}
 						else {
 							news += '<tr class="mail_unread" id="mail_' + mail_no + '" onclick="displayContent(' + mail_no + ')"><td width="10px" id="check_read_' + mail_no + '">+</td><td width="200px">' + mail_created_time + '</td><td>' + mail_title + '</td></tr>' + '<tr style="display:none;" id=' + mail_no + '><td colspan="2">' + mail_content + '</td></tr>';
 						}

					}
					$('#myContent').append('<table class="table table-striped table-hover"><thead><tr><td width="10px"></td><td width="200px">DATE</td><td>CONTENT</td></tr></thead><tbody>' + news + '</tbody></table>');
  						
				});
            }
	        function displayContent(id) {
			    if($('#mail_'+id).attr('class') == 'mail_unread') {
 			    	
			    	if(document.getElementById(id).style.display == "none") {
 			    		$('#'+id).show();
 					}
			        else{
 				        document.getElementById(id).style.display = "none";
 			       
 			   		}
 		        	
 			    	$('#mail_'+id).attr('class', 'mail_read');
 	            	$('#check_read_'+id).html('');
 
 	            	user_id = Cookies.get('user_id');
 	            	str = '/set_mail_read/' + user_id + '/';
 	            	$.post(str, { mail_no: id});
 			    }
 			    else {
 			    	if(document.getElementById(id).style.display == "none") {
 			    		$('#'+id).show();
 					}
 			        else{
 				        document.getElementById(id).style.display = "none";
 			       
 			   		}			    	
 			    }
	        }


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




