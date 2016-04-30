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
		//console.log(course)
		//console.log(maj)
		//console.log(track)
	});

	$(".add-extra-per-major-progress").each(function() {
		//console.log("HERE")
		$(this).click(function() {

			//console.log("PRINT")

			var form = $(this).children().first().attr("id")
			var list_forms = form.split("-")
			var major = list_forms[0]
			var inputstring = ".extra-major-specific-progress-"
			var res = inputstring.concat(major,"-",list_forms[1],":checked")
			var inputstring2 = "#extra-"
			var res2 = inputstring2.concat(list_forms[3],"-specific-progress-",major,"-",list_forms[1])
			var coursegrade = $(res2).val()
			var track = $(res).val()

			// from http://stackoverflow.com/questions/17149605/syntaxerror-missing-after-argument-list
			/*function quoteAndEscape(str) {
			    return ''
			        + '&#39;'                      // open quote '
			        + (''+str)                     // force string
			            .replace(/\\/g, '\\\\')    // double \
			            .replace(/"/g, '\\&quot;') // encode "
			            .replace(/'/g, '\\&#39;')  // encode '
			        + '&#39;';                     // close quote '
			}*/

			//console.log(res)
			//console.log(res2)
			//console.log($(res))
			//console.log($(res2))
			//console.log(track)
			//console.log(coursegrade)
			var dict = {'coursegrade':coursegrade,'major':major,'track':track,'morc':list_forms[3]}
			var encoded = JSON.stringify(dict)
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
		});
	});

	$(".remove-major").hide()

	refresh()
});

//console.log($(".add-extra-per-major-progress").children())

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

function remove_course() {

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
	//console.log(form)
	var dict = {'courses':form}
	var encoded = JSON.stringify(dict)
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

function update_transcript() {
    //console.log("clicked")
    	/*printme = $('#latest_transcript').html()*/
    var form = $('form').first().children('fieldset').children('input').first()[0]
    	/*console.log(form)*/
    var formdata = new FormData()
    formdata.append('transcript',form.files[0])
    	/*console.log(formdata)*/
    	/*form = $(form).children('input').first()[0]*/
    	/*console.log(form)*/
    	/*console.log(printme)*/
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
 				//console.log("here")
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
		$(obj).attr("aria-expanded","true")
	});
}

function hideCompleted() {
	$("#completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("in")
		$(obj).attr("aria-expanded","false")
	});
}

function showGpa() {
	$("#gpa").find(".panel-collapse").each(function(i,obj) {
		$(obj).addClass("in")
		$(obj).attr("aria-expanded","true")
	});
}

function hideGpa() {
	$("#gpa").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("in")
		$(obj).attr("aria-expanded","false")
	});
}

function showCertCompleted() {
	$("#certificates_completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).addClass("in")
		$(obj).attr("aria-expanded","true")
	});
}

function hideCertCompleted() {
	$("#certificates_completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("in")
		$(obj).attr("aria-expanded","false")
	});
}

function refresh() {
	$('#my-board .remove-major').show()
	$('#my-board .pin-major').hide()
	$('#recently-removed .remove-major').hide()
	$('#recently-removed .pin-major').show()
	$('.major-board').each(function(i,obj) {
		$('.remove-major')[i].onclick = function() {

			// prevent deleting permanently any majors 
			// added during the session
			var obj_id = $(obj).attr("id")
			var from_board = obj_id.startsWith("board")

			// make clone and replace with holder
			var clone = $(obj).clone()
			var holder_id = $(obj).attr('id')+"-holder"
			var id = $(obj).attr('id').substring(6)

			$("[id$="+id+"] .pin-major").each(function() {
				$(this).css("visibility","visible")
			});
			//console.log($("[id$="+id+"] .pin-major"))

			/*
			$("div[id$='"+id+"'").each(function() {
				// make pin visible
				//$(this).find(".pin-major").show()
				$(this).find("button .pin-major").css("visiblity","visible")
				console.log($(this).find("button .pin-major"))
				console.log(this)
			});*/
			/*
			if (id.startsWith("completed"))
				$(clone).find("#expansion").attr('data-parent','#completed')
			else
				$(clone).find("#expansion").attr('data-parent','#gpa')
			*/
			/*if (from_board)
				$("#recently-removed").append(clone)
			else {
				var newclone = $(obj).clone()
				$("#recently-removed").append(newclone)
				$("#"+holder_id).replaceWith(clone)
			}*/
			$(clone).find(".remove-major").hide()
			$(clone).find(".pin-major").show()

			// remove from my board
			$(obj).remove()
			refresh()
		}

		$(".pin-major")[i].onclick = function() {

			// make clone and append to board
	    	var clone = $(obj).clone()
	    	$(clone).find("#expansion").attr('data-parent','#my-board-content')
	    	$(clone).find(".remove-major").show()
	    	$(clone).find(".pin-major").hide()
	    	$("#my-board-content").append(clone)

	    	var holder = "<div id='"+$(obj).attr('id')+"-holder'></div>"
	    	$(obj).replaceWith($(holder))

	    	// basically remove all instances of that board (eg ELE) 
	    	// from the page, so you don't have one ELE board on My Board
	    	// and another in Completed etc
	    	var boardID = $(obj).attr("id")
	    	$("#selection div[id='"+boardID+"']").remove()
	    	$("#recently-removed div[id='"+boardID+"']").remove()

	    	refresh()
	    }
	});
}