// $(document).ready(function(){
$('#suggestion').keyup(function(){
		var query;
		query = $(this).val();
		$.get('/rango/suggest_category/', {suggestion: query}, function(data){
		 $('#cats').html(data);
		});
});
//});

$('#likes').click(function(){
	var catid;
	catid = $(this).attr("data-catid");
	 $.get('/rango/like_category/', {category_id: catid}, function(data){
			   $('#like_count').html(data);
			   $('#likes').hide();
		   });
});

$('.add_page_to').click(function(){
	var catid;
	var result_title;
	var result_url;
	catid = $(this).attr("data-catid");
	result_title = $(this).attr("data-title");
	result_url = $(this).attr("data-url");

	$.get('/rango/auto_add_page/',{'category_id': catid, 'url': result_url, 'title': result_title},
		function(data){
			$('.pages_container').html(data);
			
		}

	);
});
















