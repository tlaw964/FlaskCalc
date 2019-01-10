var processing = 0;

$.fn.isBefore = function(sel) {
    return this.nextAll(sel).length !== 0;
}

function sendData(string,elm) {

    var url = "{{url_for('PSupdateValues')}}"
    var form = $('#AdvancedCalculatorForm_AdvancedCalculatorForm').serializeArray();

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
                    $("form :input").removeAttr('disabled');
                    $("form :input").removeClass('disabled');
                }

                if(elm) loadingImage.remove();
                if(elm) elm.removeClass('error');


                $("input[name='InitialData']").val(data.initial_data);
                $("input[name='Flow']").val(data.avail_Wflow);
                $("input[name='UsedFlow']").val(data.Wflow);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_UsedFlow']").text(data.Wflow);
                $("input[name='PipeHead']").val(data.penstock_head);
                $("input[name='PipeLenth']").val(data.penstock_len);
                $("input[name='PipeEfficiency']").val(data.penstock_eff_target);
                $("input[name='PipeDiameter']").val(data.penstock_dia);
                $("input[name='Powerspouts']").val(data.Num_PS);
                $("input[name='Nozzles']").val(data.turbine_nozzles);
                $("input[name='JetDiameter']").val(data.jet_dia);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_JetDiameter']").text(data.jet_dia);
                $("input[name='ActualPipeEfficiency']").val(data.actual_pipe_eff);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_ActualPipeEfficiency']").text(data.actual_pipe_eff);
                $("input[name='Speed']").val(data.Opr_rpm);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_Speed']").text(data.Opr_rpm);
                $("input[name='Output']").val(data.PS_pwr_ea);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_Output']").text(data.PS_pwr_ea);
                $("input[name='TotalOutput']").val(data.Actual_turbine_electric_pwr);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_TotalOutput']").text(data.Actual_turbine_electric_pwr);
                $("input[name='OuputVoltage']").val(data.cable_Vgen);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_OuputVoltage']").text(data.cable_Vgen);
                $("input[name='CableEfficiency']").val(data.cable_eff_target);
                $("input[name='CableLength']").val(data.cable_len);
                $("input[name='LoadVoltage']").val(data.Dload_V);
                $("input[name='ActualLoadVoltage']").val(data.Aload_V);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_ActualLoadVoltage']").text(data.Aload_V);
                $("label[name='AdvancedCalculatorForm_AdvancedCalculatorForm_CableSize']").text(data.cable_mm_title); //label which changes
                $("input[name='CableSize']").val(data.cable_size);
                $("input[name='CableAWG']").val(data.cable_AWG);
                $("label[name='AdvancedCalculatorForm_AdvancedCalculatorForm_CableAWG']").text(data.cable_AWG_title);
                $("input[name='CableCurrent']").val(data.cable_amps);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_CableCurrent']").text(data.cable_amps);
                $("input[name='ActualCableEfficiency']").val(data.actual_cable_eff);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_ActualCableEfficiency']").text(data.actual_cable_eff);
                $("input[name='ActualTotalOutput']").val(data.Load_pwr);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_ActualTotalOutput']").text(data.Load_pwr);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_HydroNotes']").text(data.design_notes_hydro);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_ElecNotes']").text(data.design_notes_elec);
                $("span[id='AdvancedCalculatorForm_AdvancedCalculatorForm_SafetyNotes']").val(data.design_notes_safety);




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
sendData('firstStart');

			$(".notes .notes").each( function( index, element ){
				$( this ).html($(this).text());
			});


        $("select[name='Units']").on('change',function () {

            setTimeout(function ()  { sendData('basicdata', $("select[name='Units']")); }, 0);
        });

        $("select[name='Type']").on('change',function () {
            setTimeout(function () { sendData('PSchange', $("select[name='Type']")); }, 0);
        });

        $("input[name='Flow']").on('input',function () { setTimeout(function ()  { sendData('basicdata', $("input[name='Flow']")); }); });

        $("input[name='PipeHead']").on('input',function () {
        $this = $(this);
            setTimeout(function () { sendData('basicdata',$this); }, 2000);
        });


        $("input[name='PipeLenth']").on('input',function () {
            setTimeout(function () { sendData('penstock',   $("input[name='PipeLenth']")); }, 2000);
        });

        $("input[name='PipeEfficiency']").on('input',function () {
            setTimeout(function () { sendData('penstockeff', $("input[name='PipeEfficiency']")); }, 2000);
        });

        $("input[name='PipeDiameter']").on('input',function () {
            setTimeout(function () { sendData('pendia', $("input[name='PipeDiameter']")); }, 2000);
        });
        $("input[name='LockPipeDiameter']").on('change',function () {
            setTimeout(function () { sendData('pendiaLk',  $("input[name='LockPipeDiameter']")); }, 2000);
        });
        $("input[name='Powerspouts']").on('input',function () {
            setTimeout(function () { sendData('SetNumPSandJ', $("input[name='Powerspouts']")); }, 2000);
        });
        $("input[name='LockPowerspouts']").on('change',function () {
            setTimeout(function () { sendData('SetLkNumPSandJ',  $("input[name='LockPowerspouts']")); }, 0);
        });
        $("input[name='Nozzles']").on('input',function () {
            setTimeout(function () { sendData('SetNumPSandJ', $("input[name='Nozzles']")); }, 2000);
        });
        $("input[name='CableEfficiency']").on('input',function () {
            setTimeout(function () { sendData('SetCableEff',$("input[name='CableEfficiency']")); }, 2000);
        });
        $("input[name='CableLength']").on('input',function () {
            setTimeout(function () { sendData('NewCable',  $("input[name='CableLength']")); }, 2000);
        });
        $("input[name='LoadVoltage']").on('input',function () {
            setTimeout(function () { sendData('NewCableV',  $("input[name='LoadVoltage']")); }, 2000);
        });
        $("select[name='CableMaterial']").on('change',function () {
            setTimeout(function () { sendData('NewCableMaterial',  $("select[name='CableMaterial']")); }, 2000);
        });
        $("input[name='CableSize']").on('input',function () {
            setTimeout(function () { sendData('NewCablesize', $("input[name='CableSize']")); }, 0);
        });
        $("input[name='LockCableSize']").on('change',function () {
            setTimeout(function () { sendData('CableLock',$("input[name='LockCableSize']")); }, 0);
        });
        $("input[name='CableAWG']").on('input',function () {
            setTimeout(function () { sendData('NewCableAWG', $("input[name='CableAWG']")); }, 2000);
        });

        $("#AdvancedCalculatorForm_AdvancedCalculatorForm").submit(function(e) {


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