$(document).ready(function() {
	$('body').on('click', '.like-comment-btn', function() {
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
						$('#likes-count-' + id).text(data['likes_count']);
					} else{
						alert(JSON.parse(data).error)
					}
				}
			});
		}else {
			$.ajax({
				type: "GET",
				url: '/comments/unlike',
				data: {'comment_id': id},
				success: function(data){
					if(data['success'] == 1) {
						$('#like-btn-' + id).attr('data-like', 'like');
						$('#like-btn-' + id).text('Like');
						$('#likes-count-' + id).text(data['likes_count']);
					} else{
						alert(JSON.parse(data).error)
					}
				}
			});
		}
	});
});