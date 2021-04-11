$(function onButtonLoginClick(){
	$('button').click(function(){
		var email = $('#email-input').val();
		var password = $('#password-input').val();
		$.ajax({
			url: '/loginUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function onButtonLoginClick(response){
				console.log(response);
			},
			error: function onButtonLoginClick(error){
				console.log(error);
			}
		});
	});
});