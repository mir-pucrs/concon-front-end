$(document).ready(function(){

    // Define global variables to monitor selected norms.
    // TODO: Try to find a better way to do this.
    var global_one = null;
    var global_two = null;

    // Hide contract options while no contract is uploaded.
    $('.before_upload').hide();

    $('#selector').click(function(){

        if (global_one != null) {
            // Remove highlight over conflicting norms.
            $(global_one).removeClass('active_norm')
            $(global_two).removeClass('active_norm')
        }

        // Get the ids from the conflicting norms.
        var values = $(this).val();
        values = values.split("_")

        // Set a variable to select the table row corresponding to the norms.
        global_one = '#first_'+values[1]
        global_two = '#second_'+values[2]

        // Highlight selected norms.
        $(global_one).addClass('active_norm');
        $(global_two).addClass('active_norm');

        // Calculate the distance between the position of the selected norm and the table top.
        var ypos1 = $(global_one).offset().top - $("#first_table").height();
        
        // Make table scroll to the corresponding table row.
        $('#first_table').animate({
                scrollTop: $('#first_table').scrollTop() + ypos1 - 60
            }, 500);

        // Same process to the second norm.
        var ypos2 = $(global_two).offset().top - $("#second_table").height();
        
        $('#second_table').animate({
                scrollTop: $('#second_table').scrollTop() + ypos2 - 60
            }, 500);

        // Show correction options when a conflict is selected.
        var conflict_id = values[0];
        var norm_id_1 = values[1];
        var norm_id_2 = values[2];
        var model_name = $('#correct').attr('name');
        var html_text = "<h2>Help us!</h2><h4>Is there a conflict between norm " + norm_id_1 + " and norm " + norm_id_2 + "?<br/> If not, click below!</h4><a href=\"/conconexp/conflict/" + conflict_id + "/" + model_name + "\"><button type='button'>Not a conflict!</button>";
        $('#correct').html(html_text);
        $('#correct').css('text-align', 'center'); 
        // $('#correct').css('padding-top', '20%');
    });

    // Ensure that the user click the upload button only when he uploaded a file.
    $('#upload_button').attr('disabled','disabled');
    $('input[type="file"]').change(function(){
        if($(this).val != ''){
            $('input[type="submit"]').removeAttr('disabled');
        }
    });

    // Message to notify about the time it will take to process the contract.
    $('#file_form').submit(function() {
       alert('It may take a few minutes depending on the number of norms in the contract.');
    });

});
