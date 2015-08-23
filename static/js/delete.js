$(document).ready(function() {
      $('.comment-delete-btn').click(function(event) {
            event.preventDefault();
            var id = $(this).attr('data-id');
            if(confirm("Are you sure you want to delete this comment?")){
                  $.ajax({
                  type: "GET",
                  url: $('.comment-delete-form').attr('action'),
                  data: {'id': id, 'csrfmiddlewaretoken' : $("#csrf").attr('value')},
                  success: function(data){
                        if(data['success'] == 1) {
                              $('#comment-div-' + id).remove() 
                        }
                        else {
                              alert("You don't have permission to delete this comment")
                        }
                  }
              });
            }
      });
});