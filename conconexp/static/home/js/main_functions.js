"use strict";
$(document).ready(function(){

const time = 500;
const min_chars = 20;
class Conflict{
    constructor(){
        this.global_right = null;
        this.global_left = null;
        this.active_norm_right =null;
        this.active_norm_left = null;
        this.userId = document.querySelector('.userId').id;
        this.contractId = window.location.href.split("/")[5];
        this.values = null;
    }
    showThankMessage(){
        $('#correct').hide('#correct'); //remove "help us" part
        $('#submitNewConflict').hide('#submitNewConflict');
        $('.submitNewConflict').hide('.submitNewConflict'); 
        $('.changeText').text('Thank you!');
        $('.changeText').addClass('changeTextActive');
        $('#anotherOne').show('.anotherOne');

        $('#anotherOne').click( function(e){
            $('#correct').show('#correct'); //remove "help us" part
            $('#submitNewConflict').show('#submitNewConflict'); 
            $('.submitNewConflict').show('.submitNewConflict'); 
            $('.changeText').removeClass('changeTextActive');
            $('.changeText').text('Help Us!');
            $('#anotherOne').hide('.anotherOne');
            e.stopPropagation();
            e.stopImmediatePropagation()
        });
    }
    update(){
        if(conflicts.values != null && conflicts.global_left!=null && conflicts.global_right!=null && !($('.changeText').hasClass('changeTextActive'))){
            var conflict_id = conflicts.values[0];
            var model_name = $('#correct').attr('name');
            var html_text = "<div><h3>Is there a conflict between norm " + conflicts.global_right.split('_')[1] + " and norm " + conflicts.global_left.split('_')[1] + "?<br/> If not, click below!</h3> <button value='" + conflict_id + "' id='remove' type='button'>Not a conflict!</button></div>";
            $('#correct').html(html_text);
            $('#correct').css('text-align', 'right'); 
            $('#correct').show('#correct'); 
        }
    }
    findRightAndGlobalTwoId(){
        conflicts.active_norm_right = document.querySelector('.btn-group-right.active_norm').id;
        conflicts.global_right= document.querySelector('.btn-group-right.active_norm').id;
        conflicts.update();
    }
    findLeftAndGlobalOneId(){
        conflicts.active_norm_left = document.querySelector('.btn-group-left.active_norm').id;
        conflicts.global_left = document.querySelector('.btn-group-left.active_norm').id;
        conflicts.update();
    }
    markLeftConflicts(this2){
        var that = this2;
        if ($('.allContract-left').find('tr.active_norm').length){
            $('.allContract-left').find('tr.active_norm').toggleClass('active_norm'); //if is previously a conflict marked it unmark this and mark the new one
            $(that).addClass('active_norm');
            conflicts.findLeftAndGlobalOneId();
        }
        else{
            $(that).addClass('active_norm'); //if is there no conflict marked it marks the selected
            conflicts.findLeftAndGlobalOneId();
        }
    }
    markRightConflicts(this2){
        var that = this2;
        if ($('.allContract-right').find('tr.active_norm').length){
            $('.allContract-right').find('tr.active_norm').toggleClass('active_norm'); //if is previously a conflict marked it unmark this and mark the new one
            $(that).addClass('active_norm');
            conflicts.findRightAndGlobalTwoId();
        }
        else{
            $(that).addClass('active_norm'); //if is there no conflict marked it marks the selected
            conflicts.findRightAndGlobalTwoId();
        }
    }
    IsSameNorm(){
        if(conflicts.active_norm_left.split('_')[1] == conflicts.active_norm_right.split('_')[1] ){
            $("#error").fadeIn(time);
            $("#error article .close").click(function(e){ //click in the close modal button
                $("#error").fadeOut(time);
                e.stopPropagation();
                e.stopImmediatePropagation();
            })
            return true;
        }
        return false;
    }
    IsSameNorm2(){
        if(conflicts.global_right.split('_')[1] == conflicts.global_left.split('_')[1] ){
            $("#error").fadeIn(time);
            $("#error article .close").click(function(e){ //click in the close modal button
                $("#error").fadeOut(time);
                e.stopPropagation();
                e.stopImmediatePropagation();
            })
            return true;
        }
        return false;
    }
    showInstructions(){
        $("#instructions").fadeIn(time);
            $("#instructions article .close").click(function(e){ //click in the close modal button
                $("#instructions").fadeOut(time);
                e.stopPropagation();
                e.stopImmediatePropagation();
            })
        sessionStorage.setItem('haveSeenInstructions', true);
    }
    showSuccess(){
        $("#success").fadeIn(time);
            $("#success article .close").click(function(e){ //click in the close modal button
                $("#sucess").fadeOut(time);
                e.stopPropagation();
                e.stopImmediatePropagation();
            })
    }
    showError(){
        $("#error_conf").fadeIn(time);
            $("#error_conf article .close").click(function(e){ //click in the close modal button
                $("#error_conf").fadeOut(time);
                e.stopPropagation();
                e.stopImmediatePropagation();
            })
    }    
    removeGlobalActive(){
        $(conflicts.global_right).removeClass('active_norm');
        $(conflicts.global_left).removeClass('active_norm');
        conflicts.global_right = null;
        conflicts.global_left = null;
    }
    clearConflicts(){
        $('.allContract-right').find('tr.active_norm').removeClass('active_norm'); //clean the previous selected conflicts
        $('.allContract-left').find('tr.active_norm').removeClass('active_norm'); 
    }
    removeLeftActive(){
        $(conflicts.global_left).removeClass('active_norm');
        conflicts.global_left = null;
        $(conflicts.global_left).removeClass('active_norm');
        conflicts.global_left = null;
    }
    removeRightActive(){
        $(conflicts.global_right).removeClass('active_norm');
        conflicts.global_right= null;
        $(conflicts.global_right).removeClass('active_norm');
        conflicts.global_right = null;
    }
    reestartOptions(){
        $("select").val("none");
    }
}
class BeforeUploadContract{
    contructor(){}

    hideContractOptions(){
        // Hide contract options while no contract is uploaded.
        $('.before_upload').hide();
    }
    enableUploadButton(){
       // Ensure that the user click the upload button only when he uploaded a file.
        $('#upload_button').attr('disabled','disabled');
        $('input[type="file"]').change(function(){
            if($(this).val != ''){
                $('input[type="submit"]').removeAttr('disabled');
            }
        });
    }
    notifyWaitTime(){
        // Message to notify about the time it will take to process the contract.
        $('#file_form').submit(function() {
         alert('It may take a few minutes depending on the number of norms in the contract.');
        });
    }
}

var beforeUpload = new BeforeUploadContract();
    beforeUpload.hideContractOptions();
    beforeUpload.enableUploadButton();
    beforeUpload.notifyWaitTime();

class BeforeSubmitConflict{
    constructor(){}

    enableSubmitButton(){
        $('#submit_conflict').removeAttr('disabled');
        
    }
    disableSubmitButton(){
        $('#submit_conflict').attr('disabled', 'disabled');        
    }
}

var subConf = new BeforeSubmitConflict();
subConf.disableSubmitButton();
$('#newConflict').on('keyup', function(){
    var n_chars = this.value.length;
    if(n_chars >= min_chars){
        // Turn able the button.
        subConf.enableSubmitButton();
    }else{
        subConf.disableSubmitButton();
    }
});    

var conflicts = new Conflict();

$( "#selector" ).change(function() {
    $( "select option:selected" ).each(function() {

        if(($('.allContract-left').find('tr.active_norm').length) && ($('.allContract-right').find('tr.active_norm').length)){
                $('.allContract-right').find('tr.active_norm').removeClass('active_norm'); //clean the previous selected conflicts
                $('.allContract-left').find('tr.active_norm').removeClass('active_norm'); 
        }

        if (conflicts.global_right != null) {
            // Remove highlight over conflicting norms.
            $(conflicts.global_right).removeClass('active_norm')
            $(conflicts.global_left).removeClass('active_norm')
        }

        // Get the ids from the conflicting norms.

        conflicts.values = $(this).val().split("_");

        // Set a variable to select the table row corresponding to the norms.
        conflicts.global_right = '#first_'+conflicts.values[1];
        conflicts.global_left = '#second_'+conflicts.values[2];

        // Highlight selected norm.
        $(conflicts.global_right).addClass('active_norm');
        $(conflicts.global_left).addClass('active_norm');

        // Calculate the distance between the position of the selected norm and the table top.
        var ypos1 = $(conflicts.global_right).offset().top - $("#first_table").height();
        
        // Make table scroll to the corresponding table row.
        $('#first_table').animate({
            scrollTop: $('#first_table').scrollTop() + ypos1 - 200
        }, time);

        // Same process to the second norm.
        var ypos2 = $(conflicts.global_left).offset().top - $("#second_table").height();
        
        $('#second_table').animate({
            scrollTop: $('#second_table').scrollTop() + ypos2 - 200
        }, time);

        // Show correction options when a conflict is selected.
        conflicts.update();
    });
});


$('.btn-group-left').on('click', function(e){

    if($(this).hasClass('active_norm')){ //first of all the function check if the user is clicking in one that is already marked, if so the function unmark the correspondent cell and return 
        $(this).removeClass('active_norm');        
        conflicts.removeLeftActive();
        conflicts.reestartOptions();
        return false;
    }
    conflicts.markLeftConflicts(this);
    conflicts.reestartOptions();
    e.stopPropagation();
});

$('.btn-group-right').on('click', function(e){

       if($(this).hasClass('active_norm')){ //first of all the function check if the user is clicking in one that is already marked, if so the function unmark the correspondent cell and return 
            $(this).removeClass('active_norm');
            conflicts.removeRightActive();
            conflicts.reestartOptions();
        return false;
    }
    conflicts.markRightConflicts(this);
    conflicts.reestartOptions();
    e.stopPropagation();
});

$('#submitNewConflict').click( function(e){

    if((sessionStorage.getItem("haveSeenInstructions")) == null){
        conflicts.showInstructions();
    }

    else if(conflicts.global_right !=null && conflicts.global_left !=null ){
        if(!conflicts.IsSameNorm2()){
            //---confirm modal---//
            $("#confirm").fadeIn(time);
            $("#confirm article .close").click(function(e){ //click in the close modal button
                $("#confirm").fadeOut(time);
                e.stopPropagation();
                e.stopImmediatePropagation();
            })
            $('.confirmTheConflict').click(function(e){     //--if yes then send the norm, else leave as it was without showing thank you message--//

                console.log( "id da esquerda: " + conflicts.global_right.split('_')[1] + " " + "id da direita : " + conflicts.global_left.split('_')[1]+ " Do user: " + conflicts.userId + " Id do contrato: " + conflicts.contractId);

                var con_id = conflicts.contractId;
                var clause_id_1 = conflicts.global_right.split('_')[1];
                var clause_id_2 = conflicts.global_left.split('_')[1];
                var added_by = conflicts.userId;
                var confidence = 100;

                console.log(con_id + " " + clause_id_1 + " " + clause_id_2 + " " + added_by + " " + confidence);
                
                $.ajax({
                    url: url_sub,
                    type : "GET", // http method
                    data: {
                      'con_id': con_id,
                      'clause_id_1': clause_id_1,
                      'clause_id_2': clause_id_2,
                      'added_by': added_by,
                      'confidence': confidence
                    },
                    dataType: 'json',
                    success: function (data) {
                      if (data.done){
                        console.log("Correctly add the new conflict.");
                      }else{
                        console.log("A problem occurred when trying to add the conflict.");
                        conflicts.showError();
                        // alert("Please, inform that an error occurred while saving your conflict. Send an email to joao.aires.001@acad.pucrs.br");
                      }
                    },
                    error: function(){
                        conflicts.showError();
                    }

                });

                console.log("This ensures we made the ajax call.");

                conflicts.showThankMessage();
                conflicts.removeGlobalActive();
                conflicts.clearConflicts();
                conflicts.reestartOptions();
                $("#confirm").fadeOut(time);
                e.stopImmediatePropagation()

            })
        }
    }
    e.stopImmediatePropagation()
})

$('#remove').on('click', function(e){

    var conf_id = conflicts.values[0];

    $.ajax({
        url: url_del,
        type : "GET", // http method
        data: {
          'conf_id': conf_id
        },
        dataType: 'json',
        success: function (data) {
          if (data) {
            conflicts.showSuccess();
            setTimeout(function(){
                location.reload();
            }, 3000);
          }else{
            conflicts.showError();
          }
        }
    });

    e.stopPropagation();
});


});