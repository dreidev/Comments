$(document).ready(function() {
    $('.add-comment-form').submit(function(event){
        event.preventDefault();
        var form = $(this);
        var data =  new FormData(form.get(0));
        $.ajax({
            url: $('.add-comment-form').attr('action'),
            type: "POST",
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(json) {
                if (json['success'] == 0) {
                  errors = ""
                  for (var err in json['error']){
                    errors += "" + err + ": " + json['error'][err] + "\n"
                  }
                  alert(errors)                      
                }
                else {
                	$('#comment-input-div').prepend(json['html']);
                	$('textarea#id_comment').val(" ");
                }

            },
            error: function(response) {
            	alert("error")
            }
         });        
    });
})