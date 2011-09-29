var app = {
    centerLoginForm: function(){
        $('#login').css({
           left: $(window).width()/2 - $('#login').width()/2 
        });
    },
    showLoginForm: function(){
        $(window).resize(app.centerLoginForm);
        $('form#login').show('slide', {direction: "up"});
        
        var $form = $('#login');
        $form.submit(function(e) {
            e.preventDefault();
            $.post($form.attr('action'), $form.serialize(), function(e){
                e.preventDefault();
                $form.hide('sled', {direction: "down"});
            });
        });
    }
}

jQuery(function() {
    app.centerLoginForm(); 
    app.showLoginForm();
});
