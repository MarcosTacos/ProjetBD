$(function onButtonRegClick(){
    $('button').click(function(){
        var nom = $('#inputName').val();
        var adresse = $('#inputAddy').val();
        var telephone = $('#inputPhone').val();
        var email = $('#inputEmail').val();
        var password = $('#inputPassword').val();
        $.ajax({
            url: '/register',
            data: $('form').serialize(),
            type: 'POST',
            success: function onButtonRegClick(response){
                console.log(response);
            },
            error: function onButtonRegClick(error){
                console.log(error);
            }
        });
    });
});
