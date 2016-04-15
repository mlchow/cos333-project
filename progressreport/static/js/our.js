/*function overlay() {
	el = document.getElementById("overlay");
	el.innerHTML = ""
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}*/
$(function() {
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
            async: true,
            contentType: "application/json; charset=utf-8",
 			dataType: "text"
        });
    });
    $('#main > button#re-upload-trans').click(function() {
    	/*console.log("clicked")*/
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

    });
});