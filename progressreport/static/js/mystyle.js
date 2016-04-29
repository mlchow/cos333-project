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

	$(".remove-major").hide()

	refresh()
});

function logout() {
	$.ajax({
        url: '/logout',
        type: 'GET',
        async: true
        /*success: function(data) {
            window.location.reload(true);
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