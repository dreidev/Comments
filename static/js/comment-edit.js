$(document).ready(function() {
	
	$('.comment-edit-class').click(function(event){

		var id = $(this).attr('data-id');
		$('#comment-edit-' + id).show();
		$('#comment-' + id).hide();
});
	$('#edit-form').on('submit', function(event){
    event.preventDefault();
    var form = $(this);
    var data = $('#edit-form').serialize();
    var id = $(this).attr('data-id');
    var comment = document.getElementById('comment-'+id);
    var error = document.getElementById('edit-form-errors');

    $.ajax({
            type: "POST",
            url: $('#edit-form').attr('action'),
            data: $('#edit-form').serialize(),

            success: function(data){
                json = JSON.parse(data);
            	if(json.success == 1) {
            		comment.innerHTML = $('#id_comment').val();
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