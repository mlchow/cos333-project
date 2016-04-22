$( document ).ready(function() {

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
 		success: function() {
    		window.location.reload(true);
		}
    });
}

function exit_course_view() {
	var el = $("#overlay")[0]
	el.style.visibility = "hidden"
}

function showCompleted() {
	$("#completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("out")
		$(obj).addClass("in")
	});
}

function hideCompleted() {
	$("#completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("in")
		$(obj).addClass("out")
	});
}

function showGpa() {
	$("#gpa").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("out")
		$(obj).addClass("in")
	});
}

function hideGpa() {
	$("#gpa").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("in")
		$(obj).addClass("out")
	});
}

function showCertCompleted() {
	$("#certificates_completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("out")
		$(obj).addClass("in")
	});
}

function hideCertCompleted() {
	$("#certificates_completed").find(".panel-collapse").each(function(i,obj) {
		$(obj).removeClass("in")
		$(obj).addClass("out")
	});
}

function refresh() {
	$('.major-board').each(function(i,obj) {
		$('.remove-major')[i].onclick = function() {

			// make clone and replace with holder
			var clone = $(obj).clone()
			var holder_id = $(obj).attr('id')+"-holder"
			var id = $(obj).attr('id')
			if (id.startsWith("completed"))
				$(clone).find("#expansion").attr('data-parent','#completed')
			else
				$(clone).find("#expansion").attr('data-parent','#gpa')
			$("#"+holder_id).replaceWith(clone)
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
	    	refresh()
	    }
	});

	/*$("#show-completed").onclick = function() {
		console.log("show completed")
		$("#completed").find(".panel-collapse").each(function(i,obj) {
			$(obj).removeClass("out")
			$(obj).addClass("in")
		});
	}

	$("#hide-completed").onclick = function() {
		console.log("hide completed")
		$("#completed").find(".panel-collapse").each(function(i,obj) {
			$(obj).removeClass("in")
			$(obj).addClass("out")
		});
	}

	$("#show-gpa").onclick = function() {
		console.log("show gpa")
		$("#gpa").find(".panel-collapse").each(function(i,obj) {
			$(obj).removeClass("out")
			$(obj).addClass("in")
		});
	}

	$("#hide-gpa").onclick = function() {
		console.log("hide gpa")
		$("#gpa").find(".panel-collapse").each(function(i,obj) {
			$(obj).removeClass("in")
			$(obj).addClass("out")
		});
	}*/
}