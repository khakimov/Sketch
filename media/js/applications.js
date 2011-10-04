var app = {
    centerLoginForm: function(){
        $('#login, #register').css({
           left: $(window).width()/2 - $('#login, #register').width()/2 
        });
    },
    showLoginForm: function(){
        $(window).resize(app.centerLoginForm);
        $('form#login').show('slide', {direction: "up"});
        
        var $form = $('#login');
        $form.submit(function(e) {
            e.preventDefault();
            $('#login #errors').text('');
            
            $.post($form.attr('action'), $form.serialize(), function (e) {
                if (e.success == true ) {
                    $form.hide('slide', {direction: "up"});
                    $('#info').load('/user_info');
                    app.get_tasks();
                } else {
                    $('#login #errors').text(e.message);
                }
            });
        });
    },
    setupAjaxCallbacks: function(){
        $('body').ajaxStart(function() {
            $('#ajax-status').show().text('Loading...');
        });
        
        $('body').ajaxStop(function(){
           $('#ajax-status').fadeOut(); 
        });
        
        $('#body').ajaxError(function(e, jqxhr, settings, exception){
            console.log('XHR Response: ' + JSON.stringify(jqxhr));
        });
    },
    
    addNewTask: function(){
        $('#task-header input[type=text]').keyup(function(e){
            if(e.keyCode == 13){
            var task = $(this);
            if (task.val()){
                $.get('/add_task/', { task: task.val() }, function(e){
                    $('#tasks ul').append("<li class='task'><p id='"+ e.data +"'>"+ task.val() + "</p><span class='todo-destroy'></span></li>");
                    task.val('');
                    task.focus();
                });
            }
        }
        });
        
        $('#add').click(function(e) {
            e.preventDefault();
            var task = $('#task-header input[type=text]');
            if (task.val()){
                $.get('/add_task/', { task: task.val() }, function(e){
                    $('#tasks ul').append("<li class='task'><p id='"+ e.data +"'>"+ task.val() + "</p><span class='todo-destroy'></span></li>");
                    task.val('');
                    task.focus();
                });
            }
            return false;
        });
    },
    get_tasks: function(){
        $.get('/tasks/', function(e){
         var obj = eval('(' + e.data + ')');
         for (var i=0; i < obj.length; i++)
         {
             $('#tasks ul').append("<li class='task'><p id='"+ obj[i].pk +"'>"+ obj[i].fields.title + "</p><span class='todo-destroy'></span></li>");
         }

        });
    },
    editTask: function(attribute){
        $('.todo-destroy').live('click', function(){
            var $current = $(this).parent();
            var id = $current.find('p').attr('id');
            $.get('/del_task/', {id: id}, function(e) {
                if (e.success == true) {
                    $current.remove();
                }
            });
            return false;
        });
        
        //edit task
        $('#tasks ul li p').live('dblclick', function(e){
            var item = $(this).text();
            var element = $(this);
            var id = $(this).attr('id');
            $(this).html('<input class="textfield" name="name" tabindex="0" value="'+ item +'" type="text" />').focus();
            $('#tasks ul li p input[type=text]').keyup(function(e){
                if(e.keyCode == 13) {
                    var task = $('#tasks ul li p input[type=text]').val();
                    $.get('/update_task/', {id: id, title: task}, function(e){
                        console.log(e);
                    });
                    element.html(task);    
                }
            });
            $('#tasks ul li p input[type=text]').hover(function(){ 
                mouse_is_inside=true; 
            }, function(){ 
                mouse_is_inside=false; 
            });

            $("body").bind('mouseup', function(e){ 
                if(!mouse_is_inside) { 
                    $('body').unbind('mouseup');
                    var task = $('#tasks ul li p input[type=text]').val();
                    element.html(task);
                }
                return false;                

            });
            return false;
        });
    },
    switchLoginOrRegister: function(){
        $('#login a').click(function(e){
            e.preventDefault();
            $(window).resize(app.centerLoginForm);
            $('form#login').hide();
            $('form#register').show('slide', {direction: 'up'});
            var $form = $('#register');

            $form.submit(function(e) {
                e.preventDefault();
                $("#register label").css('color', 'white');
                $('#register #errors').text('');
                $.post($form.attr('action'), $form.serialize(), function (e) {
                    if (e.success == true ) {
                    $form.hide('slide', {direction: "up"});
                    $('#info').load('/user_info');
                    } else {
                        $('#register #errors').text(e.message);
                        if (e.data.username) { 
                            $("#register label[for='id_username']").css('color', 'red'); 
                        }
                        if (e.data.password) { 
                            $("#register label[for='id_password']").css('color', 'red'); 
                        }
                        if (e.data.email) { 
                            $("#register label[for='id_email']").css('color', 'red'); 
                        }
                    }
                });
            });

        });
        $('#register a').click(function(e){
            e.preventDefault();
            $('form#register').hide();
            app.showLoginForm();
        });
    }
}

var mouse_is_inside = false;

jQuery(function() {
    app.setupAjaxCallbacks();
    app.centerLoginForm(); 
    // check auth status and show Login form or load information about user.
    $('#info').load('/user_info', function(responseText, textStatus, XMLHttpRequest) {
       if (textStatus == "error") {
           app.showLoginForm();
       } else { 
           app.get_tasks();
       }

    });
    app.addNewTask();
    app.editTask();
    app.switchLoginOrRegister();

    


});
