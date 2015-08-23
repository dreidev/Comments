$(document).ready(function() {
      $('body').on('click', '.comment-delete-btn', function(event) {
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
                              if (data['count'] == 0) {
                                    $('#no-comments').show()
                              }
                              else {
                                    $('#no-comments').hide()
                              }
                        }
                        else {
                              alert("You don't have permission to delete this comment")
                        }
                  }
              });
            }
      });
});