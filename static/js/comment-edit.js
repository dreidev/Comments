$(document).ready(function() {
	
	$('body').on('click', '.comment-edit-class', function(event){

		var id = $(this).attr('data-id');
		$('#comment-edit-' + id).show();
		$('#comment-' + id).hide();
    });

	$('body').on('submit', '.edit-form', function(event){
    event.preventDefault();
    var form = $(this);
    var data = form.serialize();
    var id = $(this).attr('data-id');
    var comment = document.getElementById('comment-'+id);
    var error = document.getElementById('edit-form-errors');
    $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: data,

            success: function(data){
                json = JSON.parse(data);
            	if(json.success == 1) {
            		comment.innerHTML = $('#input-comment-' + id).val();
            		$('#comment-edit-' + id).hide();
            		$('#comment-' + id).show();
            	} else if(json.success == 0){
                     errors = ""
                  for (var err in json.error){
                    errors += "" + json.error[err] + "\n";
                }
                error.innerHTML = errors;
            }
            },
            dataType: 'html'
        });
    });

})