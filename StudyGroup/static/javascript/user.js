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
					var mission ='';
					for(var i = 0; i < mission_list.length; i++) {
						mission_no = mission_list[i];
						mission = '<a class="missionBox" href="#name_checking_div" onclick="renderMission(' + mission_no + ')"><div class="list-group-item row"><h4 align="center">Mission from System</h4></div></a>';
						
					}

					$('#myContent').append(mission);
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
		            	name += '<button type="button" onclick="checkAns(\'' + name_list[i] + '\')">' + name_list[i] + '</button>';
		            }
		            
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

			function checkAns (input) {
				if(input == ans) {
					alert('you got it right');	
				}
				else {
					alert('wrong answerQQ')
				}
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
							news += '<tr class="mail_read" onclick="displayContent(' + mail_no + ')"><td>' + mail_created_time + '</td><td>' + mail_title + '</td></tr>' + '<tr class="news_content" id=' + mail_no + '><td colspan="2">' + mail_content + '</td></tr>';
						}
						else {
							news += '<tr class="mail_unread" onclick="displayContent(' + mail_no + ')"><td>' + mail_created_time + '</td><td>' + mail_title + '</td></tr>' + '<tr class="news_content" id=' + mail_no + '><td colspan="2">' + mail_content + '</td></tr>';
						}

					}
					$('#myContent').append('<table class="table table-striped table-hover"><thead><tr><td>DATE</td><td>CONTENT</td></tr></thead><tbody>' + news + '</tbody></table>');
					console.log(data);
				});
            }
	        function displayContent(id) {
			    if($(this).attr('className') == 'mail_unread') {
			    	$(this).attr('className') = 'mail_read';
	            	
	            	user_id = Cookies.get('user_id');
	            	str = '/set_mail/' + user_id + '/';
		            $.post(str, { mail_no: id}).then(function () {
					    window.location = '/get_mail/'+ user_id;
				    });
			    }

		        if(document.getElementById(id).style.display == "none") {
			        $('#'+id).show();
		        }
		        else
			        document.getElementById(id).style.display = "none";
	        }