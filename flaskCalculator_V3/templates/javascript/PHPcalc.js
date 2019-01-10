var processing = 0;

$.fn.isBefore = function(sel) {
    return this.nextAll(sel).length !== 0;
}

function sendData(string,elm) {

    var url = "{{url_for('PHPupdateValues')}}"
    var form = $('#AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm').serializeArray();

    var loadingImage = $("<img class='loading' src='{{url_for('static', filename='assets/ajax-loader.gif')}}'/>");
    if((elm) && elm.isBefore(".loading")) { loadingImage.insertAfter(elm); }



    form.push({ name: 'processOption', value: string });


$('input[type=checkbox]').each(function() {
    if (!this.checked) {
        form.push({ name: this.name, value: 0 });
    }
});
    var data = {};
    $(form).each(function (index, obj) {
        data[obj.name] = obj.value;
    });


    window.console && console.log(data);

        $.ajax({
            type: "POST",
            url: url,
            data: form, // serializes the form's elements.
            success: function (data) {
                console.log('Submission was successful.');
                console.log(JSON.parse(data));
                data = JSON.parse(data)

                //if inital data is no longer false un hide all the hidden fields
                if (data.initial_data == 0) {

                }

                if(elm) loadingImage.remove();
                if(elm) elm.removeClass('error');


                $("input[name='meas_sys']").val(data.meas_sys);
                $("input[name='available_input_flow']").val(data.available_input_flow);
                $("input[name='actual_IP_flow']").val(data.actual_IP_flow);
                $("span[id='AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm_actual_IP_flow']").text(data.actual_IP_flow);
                $("input[name='input_head']").val(data.input_head);
                $("input[name='input_pipe_len']").val(data.input_pipe_len);
                $("input[name='input_eff']").val(data.input_eff);
                $("input[name='input_pipe_diam']").val(data.input_pipe_diam);
                $("input[name='lock_penstock_dia']").val(data.lock_penstock_dia);
                $("input[name='number_of_spouts']").val(data.number_of_spouts);
                $("input[name='number_of_jets']").val(data.number_of_jets);
                $("input[name='lock_PHPs_jets']").val(data.lock_PHPs_jets);

                $("input[name='eff_input_head']").val(data.eff_input_head);
                $("span[id='AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm_eff_input_head']").text(data.eff_input_head);

                $("input[name='jet_diam']").val(data.jet_diam);
                $("span[id='AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm_jet_diam']").text(data.jet_diam);

                $("input[name='pelton_rpm']").val(data.pelton_rpm);
                $("span[id='AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm_pelton_rpm']").text(data.pelton_rpm);

                $("input[name='cam_offset']").val(data.cam_offset);
                $("span[id='AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm_cam_offset']").text(data.cam_offset);

                $("input[name='PHP_deliver_h']").val(data.PHP_deliver_h);
                $("span[id='AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm_PHP_deliver_h']").text(data.PHP_deliver_h);

                $("input[name='output_head']").val(data.output_head);
                $("input[name='output_pipe_len']").val(data.output_pipe_len);
                $("input[name='output_eff']").val(data.output_eff);
                $("input[name='output_pipe_diam']").val(data.output_pipe_diam);
                $("input[name='lock_OP_pipe_dia']").val(data.lock_OP_pipe_dia);

                $("input[name='total_OP_flow']").val(data.total_OP_flow);
                $("span[id='AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm_total_OP_flow']").text(data.total_OP_flow);

                $("input[name='total_OP_flow_day']").val(data.total_OP_flow_day);
                $("span[id='AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm_total_OP_flow_day']").text(data.total_OP_flow_day);

                $(".notes .notes").each( function( index, element ){
                         var v = $(this).text();
                         if (v == "") {
                                  $(this).parent().parent().hide(); //if empty
                         }else{
                            $(this).parent().parent().show();
							$(this).html(v);
							$(this).next().val(v);
                         }
                });


            },
            error: function (data) {
                if(elm) loadingImage.remove();
				elm.addClass('error');
            },
        });
var processing = 0;
}

function inputURL() {
// Code for dealing with a link containing the url parameters
//grab the entire query string
var query = document.location.search.replace('?', '');

//extract each field/value pair
query = query.split('&');

//run through each pair
for (var i = 0; i < query.length; i++) {

  //split up the field/value pair into an array
  var field = query[i].split("=");

//email doesnt work for some reason
  if (field[0] == 'Email'){ continue; }

  //target the field and assign its value
  $("input[name='" + field[0] + "'], select[name='" + field[0] + "']").val(field[1]);
}

}


$(document).ready(function () {


inputURL(); //if the user has clicked on the URL in the email which has stored their data this will input it to the form
sendData('default');

			$(".notes .notes").each( function( index, element ){
				$( this ).html($(this).text());
			});


        $("input[name='meas_sys']").on('change',function () {

            setTimeout(function () { sendData('units', $("select[name='meas_sys']")); }, 0);
        });

        $("input[name='available_input_flow']").on('input',function () {
            setTimeout(function () { sendData('available_input_flow', $("select[name='available_input_flow']")); }, 2000);
        });

        $("input[name='input_head']").on('input',function () {
            setTimeout(function () { sendData('input_head', $("input[name='input_head']")); }, 2000);
        });

        $("input[name='input_pipe_len']").on('input',function () {
            setTimeout(function () { sendData('input_pipe_len',   $("input[name='input_pipe_len']")); }, 2000);
        });

        $("input[name='input_eff']").on('input',function () {
            setTimeout(function () { sendData('input_pipe_eff', $("input[name='input_eff']")); }, 2000);
        });

        $("input[name='input_pipe_diam']").on('input',function () {
            setTimeout(function () { sendData('input_pipe_diam', $("input[name='input_pipe_diam']")); }, 2000);
        });
        $("input[name='lock_penstock_dia']").on('change',function () {
            setTimeout(function () { sendData('input_pipe_lock',  $("input[name='lock_penstock_dia']")); }, 0);
        });
        $("input[name='number_of_spouts']").on('input',function () {
            setTimeout(function () { sendData('number_of_spouts', $("input[name='number_of_spouts']")); }, 2000);
        });
        $("input[name='lock_PHPs_jets']").on('change',function () {
            setTimeout(function () { sendData('PHPs_lock',  $("input[name='lock_PHPs_jets']")); }, 0);
        });
        $("input[name='number_of_jets']").on('input',function () {
            setTimeout(function () { sendData('number_of_jets', $("input[name='number_of_jets']")); }, 2000);
        });


        $("input[name='output_head']").on('input',function () {
            setTimeout(function () { sendData('output_head', $("input[name='output_head']")); }, 2000);
        });
                $("input[name='output_pipe_len']").on('input',function () {
            setTimeout(function () { sendData('output_pipe_len', $("input[name='output_pipe_len']")); }, 2000);
        });

        $("input[name='output_eff']").on('input',function () {
            setTimeout(function () { sendData('output_pipe_eff', $("input[name='output_eff']")); }, 2000);
        });
                $("input[name='output_pipe_diam']").on('input',function () {
            setTimeout(function () { sendData('output_pipe_diam', $("input[name='output_pipe_diam']")); }, 2000);
        });
                $("input[name='lock_OP_pipe_dia']").on('change',function () {
            setTimeout(function () { sendData('lock_OP_pipe_dia', $("input[name='lock_OP_pipe_dia']")); }, 0);
        });

        $("#AdvancedCalculatorPumpForm_AdvancedCalculatorPumpForm").submit(function(e) {


            var form = $(this);
            var url = form.attr('action');

            if( $('select[name="Dealer"]').val() == '0' ){
               $(".alert").css("background-color", "##ff9800");
               $("#alertText").html('You must select a dealer! To find which dealer is best for you please click <a target="_blank" rel="noopener noreferrer" href="https://www.powerspout.com/collections/find-a-dealer-1">here</a>');
               $(".alert").show();
               e.preventDefault();
               return;
            }

            $(".alert").css("background-color", "#2196F3");
           $("#alertText").text('Loading! Submitting you site information ......');
            $(".alert").show();

            $.ajax({
                   type: "POST",
                   url: url,
                   data: form.serialize(), // serializes the form's elements.
                   success: function(data)   {
                     data = JSON.parse(data);

                     if (data.errors == 1){
                     $(".alert").css("background-color", "#f44336");
                     $("#alertText").text(data.message); //sucsess
                     }else{
                     $(".alert").css("background-color", "#4CAF50");
                     $("#alertText").text(data.message); //sucsess
                     }
                   },
                    error: function (data) {
                     $(".alert").css("background-color", "#f44336");
                     $("#alertText").text('Error code 3: Something went wrong with submitting your data please contact admin@ecoinnovation.co.nz for support');
                     },
                 });

            e.preventDefault(); // avoid to execute the actual submit of the form.
        });



});