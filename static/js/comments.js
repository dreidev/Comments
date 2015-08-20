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
                	html = "<div class='comment'> Comment:"+ json['comment'] + "<br> Likes: {{ object.likes_count }}<br></div>"
					$('body').append(html)
                }

            },
            error: function(response) {
            	alert("error")
            }
         });        
    });
})