
$(document).ready(function () {
	        
	//goTop
	$(window).scroll(function(){
		if ($(this).scrollTop() > 250) {
			$('#gotop').fadeIn();
		} else {
			$('#gotop').fadeOut();
		}
	});
	//Click event to scroll to top
	$('#gotop').click(function(){
		$('html, body').animate({scrollTop : 0},800);
		return false;
	});

	//Click event to scroll to top
	$('#account_btn').click(function(){
		$('#account_menu').slideToggle(200);
	});


});
