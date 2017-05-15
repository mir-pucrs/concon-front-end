$(document).ready(function(){

    var global_one = null;
    var global_two = null;

    $('.before_upload').hide();
    
    
    $('#selector').click(function(){

        if (global_one != null) {

            $(global_one).css("background-color", "white")
            $(global_two).css("background-color", "white")

        }

        var values = $(this).val();

        values = values.split("_")

        
        // first_conflict = $('#conflict').attr('value')
        // second_conflict = $('#conflict').attr('name')

        $('#first_'+values[0]).css("background-color", "#ff6666");

        $('#second_'+values[1]).css("background-color", "#ff6666");

        global_one = '#first_'+values[0]
        global_two = '#second_'+values[1]

    });

    $('#upload_button').attr('disabled','disabled');
    $('input[type="file"]').change(function(){
        if($(this).val != ''){
            $('input[type="submit"]').removeAttr('disabled');
        }
    });

    $('#file_form').submit(function() {

	alert('It may take a few minutes depending on the number of norms in the contract.');

    });


    
    // $("#login_button").click(function(){
        
    //     $.post("login.php",
    //     {
    //       username: $("#name").val(),
    //       password: $("#password").val()
    //     },
    //     function(data,status){

    //         if(data){
              
    //             swal({
    //               title: 'Success!',
    //               text: 'Logged in.',
    //               type: 'success',
    //               confirmButtonText: 'OK'
    //             }, function(isConfirm) {
    //                 window.location.replace('index.php');
    //             });
                
    //         }else{
                
    //             swal({
    //               title: 'Error!',
    //               text: 'Your username or password is wrong.',
    //               type: 'error',
    //               confirmButtonText: 'OK'
    //               }, function(isConfirm) {
    //                   location.reload();
    //             });
                
    //         }

    //     });
        
    // });

    // $("#register_button").click(function(e){

    //     var name = $("#name_reg").val();
    //     var username = $("#username_reg").val();
    //     var email = $("#email").val();
    //     var password1 = $("#passwordN1").val();
    //     var password2 = $("#passwordN2").val();
    //     var email_ok = validate_email(email);

    //     if(name === "" || username === "" || email === "" || password1 === "" || password2.length === ""){
    //         swal({
    //           title: 'Oops!',
    //           text: 'All fields are required.',
    //           type: 'warning',
    //           confirmButtonText: 'OK'
    //         })
    //     }
    //     else if (password1 != password2) {
    //         swal({
    //             title: 'Oops!',
    //             text: 'Your password and confirmation must be the same.',
    //             type: 'warning',
    //             confirmButtonText: 'OK'
    //         });
    //     }else if(!email_ok){
    //         swal({
    //             title: 'Oops!',
    //             text: 'You need to insert a valid email.',
    //             type: 'warning',
    //             confirmButtonText: 'OK'
    //         });
    //     }else{
    //         $.post("register.php",
    //         {
    //           name: $("#name_reg").val(),
    //           username: $("#username_reg").val(),
    //           email: $("#email").val(),
    //           password1: $("#passwordN1").val(),
    //           password2: $("#passwordN2").val(),
    //         },
    //         function(data,status){
    //             if(data){
    //                 swal({
    //                   title: "Success!",
    //                   text: "User registered!",
    //                   type: 'success',
    //                   confirmButtonText: 'OK'
    //                 });  
    //             }
    //         });
    //     }

    //     e.preventDefault();

    // });

    // $("#upload_button").click(function(e){

    //     var file_data = $('#fileToUpload').prop('files')[0];

    //     if (!file_data){
    //         swal({
    //           title: "Oops!",
    //           text: "Please choose a file first.",
    //           type: 'warning',
    //           confirmButtonText: 'OK'
    //         });
    //     }else{
    //         var form_data = new FormData();                  
    //         form_data.append('file', file_data);
    //         $.ajax({
    //             url: 'upload.php', // point to server-side PHP script 
    //             dataType: 'text',  // what to expect back from the PHP script, if anything
    //             cache: false,
    //             contentType: false,
    //             processData: false,
    //             data: form_data,                         
    //             type: 'post',
    //             success: function(data){
    //                 if (data == 'ALREADY') {
    //                     swal({
    //                       title: "Oops!",
    //                       text: "This file already exists.",
    //                       type: 'warning',
    //                       confirmButtonText: 'OK'
    //                     });
    //                 } else if (data == 'FORMAT') {
    //                     swal({
    //                       title: "Oops!",
    //                       text: "File format not accepted. Please insert a .txt or .md",
    //                       type: 'warning',
    //                       confirmButtonText: 'OK'
    //                     });
    //                 } else if (data == 'ERROR') {
    //                     swal({
    //                       title: "Error!",
    //                       text: "Sorry, we had a problem while processing the file. Try again later.",
    //                       type: 'warning',
    //                       confirmButtonText: 'OK'
    //                     });
    //                 } else if (data == 'SUCESS') {
    //                     swal({
    //                       title: "Success!",
    //                       text: "File uploaded!",
    //                       type: 'success',
    //                       confirmButtonText: 'OK'
    //                     });
    //                 }
    //             }
    //         });
    //     }
    // });
});
