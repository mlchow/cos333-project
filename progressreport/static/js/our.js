/*function overlay() {
	el = document.getElementById("overlay");
	el.innerHTML = ""
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}*/
$(function() {
    /*$('#logout-button').click(function() {
        $.ajax({
            url: '/logout',
            type: 'GET',
            async: true,
            success: function(data) {
                window.location.reload(true);
            }
        });
    });*/
    $('#submit-my-board').click(function() {
    	var lis = []
    	$('#my-board-content').children('div').each(function() {
    		var txt = $(this).html()
    		pattern = /\<b\>[A-Z][A-Z][A-Z]\<\/b\>/
    		match = pattern.exec(txt)
    		lis.push(match[0].slice(3,match[0].length-4))
    	});
    	/*console.log("clicked")*/
    	dict = {"majors":lis}
    	var encoded = JSON.stringify(dict)
    	/*console.log(encoded)*/
        $.ajax({
            url: '/updateinterests',
            data: encoded,
            type: 'POST',
            contentType: "application/json; charset=utf-8",
 			dataType: "text"
        });
        $.ajax({
            url: '/suggestcourses',
            data: encoded,
            contentType: "application/json; charset=utf-8",
            dataType: "text",
            type: 'POST',
            success: function(data) {
                var data = JSON.parse(data)
                var suggested_courses = data['suggested_courses']
                var txt = "Courses we would recommend for you based on your interests... <br />"
                //console.log(suggested_courses)
                //console.log(suggested_courses)
                for (i = 0; i < suggested_courses.length; i++) {
                    if (suggested_courses[i][0].length > 0) {
                        if (suggested_courses[i][0][2].length > 0) {
                            txt = txt + suggested_courses[i][0] + " fulfills... "
                            var lst = [];
                            for (k = 0; k < suggested_courses[i][2].length; k++) {
                                //if (lst.indexOf(suggested_courses[i][2][k]) < 0) {
                                txt = txt + suggested_courses[i][2][k] + " "
                                lst.push(suggested_courses[i][2][k])
                                //}
                            }
                            txt = txt + "<br />"
                        }
                    }
                }
                $("#suggested_courses").html(txt)
            }
        });
    });
    /*$('#re-upload-trans').click(function() {
    	console.log("clicked")
    	/*printme = $('#latest_transcript').html()
    	var form = $('form').first().children('fieldset').children('input').first()[0]
    	/*console.log(form)
    	var formdata = new FormData()
    	formdata.append('transcript',form.files[0])
    	/*console.log(formdata)
    	/*form = $(form).children('input').first()[0]
    	/*console.log(form)
    	/*console.log(printme)
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

    });*/
    /*$('#exit_view_course').click(function() {
    	console.log("EXIT")
    	var el = $("#overlay")[0]
		el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible"
    });*/
    $('tr:not(.info)').each(function() {
    	// maybe we should change click to hover
		$(this).children("td").first().click(function() {
			var name = $(this).text()
			dict = {"coursename":name}
	    	var encoded = JSON.stringify(dict)
	    	/*console.log(encoded)*/
	        $.ajax({
	            url: '/viewcourse',
	            data: encoded,
	            type: 'POST',
	            async: true,
	            contentType: "application/json; charset=utf-8",
	 			dataType: "text",
	 			success: function(data) {
	 				/*console.log("here")
	 				console.log(data)*/
	 				var data = JSON.parse(data)
	 				var int_maj = data['interested_majors']
	 				var html = "<button type='button' onclick='exit_course_view()' class='btn btn-info' id='exit_view_course'>Hide</button>"
                    html = html + "<br />" + name + " is currently fulfilling requirements in the following areas of interest for you...<br />"
	 				if (int_maj != undefined){
	 					for (i=0;i<int_maj.length;i++)
	 						html = html + "<b>" + int_maj[i] + "</b><br />"
	 				}
	 				int_maj = data['interested_certificates']
	 				if (int_maj != undefined){
	 					for (i=0;i<int_maj.length;i++)
	 						html = html + "<b>" + int_maj[i] + "</b><br />"
	 				}
	 				int_maj = data['others']
	 				if (int_maj != undefined){
	 					html = html + "<br />" + name + " could also fulfill requirements in these areas among others...<br />"
	 					for (i=0;i<int_maj.length && i < 5;i++)
	 						html = html + int_maj[i] + "<br />"
	 				}
					$("#overlay").html(html)
					var el = $("#overlay")[0]
					el.style.visibility = "visible"
	 			}
	        });
		});
	});
});