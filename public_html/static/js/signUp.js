$(function() {
    $('#btnSignUp').click(function() {
        console.log("This is working so far");
        $.ajax({
            url: '/RegisterUser',
            data: $('form').serialize(),
            console:log(data),
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