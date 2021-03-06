var alphanumspace = /^[0-9a-zA-Z\s,\+-]+$/;

$( document ).ready(function() {

	$(".glyphicon-remove").click(function() {
		course_grade = $(this).parent().parent().text()
		maj_req = $(this).attr("name").split("-")
		course = course_grade.substring(0,6)
		maj = maj_req[0]
		track = maj_req[1]
		mc = maj_req[2]
		$(this).parent().parent().remove()
		var dict = {'course':course,'major':maj,'track':track,'type':mc}
		var encoded = JSON.stringify(dict)
		$.ajax({
	    	url: '/deletemanualprogress',
	     	data: encoded,
	    	type: 'POST',
	    	async: true,
	    	contentType: "application/json; charset=utf-8",
		 	dataType: "text",
    	});
	});

	$(".add-extra-per-major-progress").each(function() {
		//console.log("HERE")
		$(this).click(function() {
			var form = $(this).children().first().attr("id")
			var list_forms = form.split("-")
			var major = list_forms[0]
			var inputstring = ".extra-major-specific-progress-"
			var res = inputstring.concat(major,"-",list_forms[1],":checked")
			var inputstring2 = "#extra-"
			var res2 = inputstring2.concat(list_forms[3],"-specific-progress-",major,"-",list_forms[1])
			var coursegrade = $(res2).val()
			var track = $(res).val()

			var dict = {'coursegrade':coursegrade,'major':major,'track':track,'morc':list_forms[3]}
			var encoded = JSON.stringify(dict)
			if (coursegrade.match(alphanumspace)) {
				$.ajax({
			    	url: '/addmajormanualprogress',
			     	data: encoded,
			    	type: 'POST',
			    	async: true,
			    	contentType: "application/json; charset=utf-8",
				 	dataType: "text",
				 	success: function(data) {
				 		var data = JSON.parse(data)
	                	var courses = data['courses']
				 		for (var i = 0; i < courses.length; i++) {
				 			var toselect = "#"
				 			var restoselect = toselect.concat(major,"-",track,"-info-",list_forms[1])
				 			c = courses[i][0]
				 			g = courses[i][1]
				 			var toadd = "<tr><td>"
				 			var toaddmore = toadd.concat(c,"</td><td>",g,"</td>")
				 			var toadd2 = toaddmore.concat('<span name=\\&quot;',major,'-',track,'-',list_forms[3][0],'\\&quot;')
				 			var toadd3 = toadd2.concat('class=\\&quot;glyphicon glyphicon-remove\\&quot; aria-hidden=\\&quot;true\\&quot;></span></td></tr>')
				 			//console.log(toadd3)
				 			if ($(restoselect).length) {
				 				$(restoselect).after(toadd3)
				 			}
				 			else {
				 				toselect = "table#"
				 				restoselect = toselect.concat(major,"-",list_forms[1])
				 				var newrowheader = '<tr class=info id='
				 				var addme = newrowheader.concat(major,'-',track,'-info-',list_forms[1],'><th style=background-color:#d9edf7;border: 1px solid #ddd;padding:5px; colspan=2>',track,'</th></tr>',toadd3)
				 				$(restoselect).children().first().before(addme)
				 			}

				 		}
				 	}
			    });
			}
			else {
				
			}
		});
	});

	$(".remove-major").hide()

	refresh()
});

function logout() {
	$.ajax({
        url: '/logout',
        type: 'GET',
        async: true
        /*success: function() {
           	$("#real-logout").click()
        }*/
    });
}

function delete_acc() {
	$.ajax({
        url: '/deleteaccount',
        type: 'GET',
        async: true
        /*success: function(data) {
            window.location.reload(true);
        }*/
    });
}

function add_to_progress() {
	var form = $("#extra-courses").val() //.children('fieldset').children('input').first().val()
	var dict = {'courses':form}
	var encoded = JSON.stringify(dict)
	if (form.match(alphanumspace)) {
		$("#mistake").html("");
		$.ajax({
	    	url: '/addmanualprogress',
	     	data: encoded,
	    	type: 'POST',
	    	async: true,
	    	contentType: "application/json; charset=utf-8",
		 	dataType: "text",
	 		success: function(data) {
	 			window.location.reload(true);
	 			/*$.ajax({
	        		url: '/refreshandreloadpage',
	        		type: 'GET',
	        		async: true
	    		});*/
			}
	    });
	}
	else {
		$("#mistake").text("Oops! This doesn't look like a correctly formatted list of courses to us! Please check the example.")
	}

}

function update_transcript() {
    var form = $('form').first().children('fieldset').children('input').first()[0]
    var formdata = new FormData()
    formdata.append('transcript',form.files[0])

	$.ajax({
    	url: '/updatetranscript',
     	data: formdata,
    	type: 'POST',
    	async: true,
    	contentType: false,
 		processData: false,
 		success: function(data) {
 			var data = JSON.parse(data)
 			if (data['correctfile'] == 'No') {
 				$('#mistake').text("Oops! This doesn't look like your transcript to us. Double check that you are uploading your unencrypted unofficial transcript as a pdf and please upload again.")
 			}
 			else {
 				window.location.reload(true);
 				//$.ajax({})
 				/*$.ajax({
	        		url: '/refreshandreloadpage',
	        		type: 'GET',
	        		async: true
	    		});*/
 			}
		}
    });
}

function exit_course_view() {
	var el = $("#overlay")[0]
	el.style.visibility = "hidden"
}

function showCompleted() {
	$("#completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).addClass("in")
		$(obj).removeAttr("style")
		$(obj).attr("aria-expanded","true")
	});
}

function hideCompleted() {
	$("#completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("in")
		$(obj).removeAttr("style")
		$(obj).attr("aria-expanded","false")
	});
}

function showGpa() {
	$("#gpa").find(".panel-collapse").each(function(i,obj) {
		$(obj).addClass("in")
		$(obj).removeAttr("style")
		$(obj).attr("aria-expanded","true")
	});
}

function hideGpa() {
	$("#gpa").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("in")
		$(obj).removeAttr("style")
		$(obj).attr("aria-expanded","false")
	});
}

function showCertCompleted() {
	$("#certificates_completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).addClass("in")
		$(obj).removeAttr("style")
		$(obj).attr("aria-expanded","true")
	});
}

function hideCertCompleted() {
	$("#certificates_completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("in")
		$(obj).removeAttr("style")
		$(obj).attr("aria-expanded","false")
	});
}

function refresh() {
	/*$('.panel-collapse').css("height","")*/

	$('#my-board .remove-major').show()
	$('#my-board .pin-major').hide()

	$('.major-board').each(function(i,obj) {
		$('.remove-major')[i].onclick = function() {
			// show all major PIN buttons
			var maj_id = $(obj).attr('id')
	    	maj_id = maj_id.substring(maj_id.length - 3)
	    	//console.log("id: "+maj_id)
	    	//console.log($(".major-"+maj_id))
			$(".major-"+maj_id).each(function(obj) {
				$(this).find(".pin-major").each(function() {
					$(this).css("visibility","visible")
					$(this).css("display","")
				})
			})

			// remove from my board
			$(obj).remove()
			refresh()
		}

		$(".pin-major")[i].onclick = function() {

			// make clone and append to board
	    	var clone = $(obj).clone()
	    	$(clone).find("#expansion").attr('data-parent','#my-board-content')
	    	$(clone).find(".remove-major").show()
	    	$("#my-board-content").append(clone)

	    	var maj_id = $(obj).attr('id')
	    	maj_id = maj_id.substring(maj_id.length - 3)
	    	$(".major-"+maj_id).find(".pin-major").hide()

	    	refresh()
	    }
	});
}