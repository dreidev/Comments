$(document).ready(function() {
    // ADD COMMENT //
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
                    var comment_count = document.getElementById('comments-count');
                    if (parseInt(comment_count.innerHTML) == 0) {
                        comment_count.innerHTML = parseInt(comment_count.innerHTML) + 1 + " Comment";
                    } else {
                        comment_count.innerHTML = parseInt(comment_count.innerHTML) + 1 + " Comments";
                    }
                    html = "<div id='comment-div-" + json['id'] + "'>" +json['html'] +"</div>"
                	$('.comments').append(html);
                	$('textarea#id_comment').val(" ");
                    $('#no-comments').hide()
                }

            },
            error: function(response) {
            	alert("error")
            }
         });        
    });
    
    // DELETE COMMENT //
    $('.comments-wrapper').on('click', '.comment-delete-btn', function(event) {
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

    // COMMENT EDIT //
    $('.comments-wrapper').on('click', '.comment-edit-class', function(event){

        var id = $(this).attr('data-id');
        $('#comment-edit-' + id).show();
        $('#comment-' + id).hide();
    });

    $('.comments-wrapper').on('submit', '.edit-form', function(event){
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


    // LIKE UNLIKE COMMENT //
    $('.comments-wrapper').on('click', '.like-comment-btn', function() {
        var id = $(this).attr('data-id');
        if($(this).attr('data-like') == 'like') {
            $.ajax({
                type: "GET",
                url: '/comments/like',
                data: {'comment_id': id},
                success: function(data){
                    if(data['success'] == 1) {
                        $('#like-btn-' + id).attr('data-like', 'liked');
                        $('#like-btn-' + id).text('Unlike');
                        $('#likes-count-' + id).text("Likes: " + data['likes_count']);
                    } else{
                        alert(data['error']);
                    }
                }
            });
        } else {
            $.ajax({
                type: "GET",
                url: '/comments/unlike',
                data: {'comment_id': id},
                success: function(data){
                    if(data['success'] == 1) {
                        $('#like-btn-' + id).attr('data-like', 'like');
                        $('#like-btn-' + id).text('Like');
                        $('#likes-count-' + id).text("Likes: " + data['likes_count']);
                    } else{
                        alert(data['error']);
                    }
                }
            });
        }
    });

})