$(function() {
    $('#btnSignIn').click(function() {
        console.log("This is working so far");
        $.ajax({
            url: '/validateLogin',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});