$(document).ready(function() {
	$('.comment-delete-btn').click(function(event) {
		event.preventDefault();
		var id = $(this).attr('data-id');

		$.ajax({
                  type: "GET",
                  url: $('.comment-delete-form').attr('action'),
                  data: {'id': id, 'csrfmiddlewaretoken' : $("#csrf").attr('value')},
                  success: function(data){
                  	if(data['success'] == 1) {
                  		$('#comment-div-' + id).remove() 
                  	}
                  }
            });
	});
});