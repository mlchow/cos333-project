$( document ).ready(function() {

	$(".remove-major").hide()

	refresh()
});

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