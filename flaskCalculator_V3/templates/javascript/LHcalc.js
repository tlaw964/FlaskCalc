var processing = 0;

$.fn.isBefore = function(sel) {
    return this.nextAll(sel).length !== 0;
}

function sendData(string,elm) {

    var url = "{{url_for('LHupdateValues')}}"
    var form = $('#AdvancedCalculatorLHForm_AdvancedCalculatorLHForm').serializeArray();

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
                $("input[name='AvailLPS']").val(data.avail_lps);
                $("input[name='ActualLPS']").val(data.actual_lps);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_ActualLPS']").text(data.actual_lps);
                $("input[name='LHHead']").val(data.LH_head);
                $("input[name='PipeHead']").val(data.pipe_head);
                $("input[name='PipeDia']").val(data.pipe_dia);
                $("input[name='PipeHeight']").val(data.pipe_height);
                $("input[name='PipeLen']").val(data.pipe_len);
                $("input[name='WaterDepth']").val(data.water_depth);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_WaterDepth']").text(data.water_depth);
                $("input[name='PipeCapacity']").val(data.pipe_capacity);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeCapacity']").text(data.pipe_capacity);
                $("input[name='LHDraftT']").val(data.LH_Draft_T);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_LHDraftT']").text(data.LH_Draft_T);
                $("input[name='NumLH']").val(data.Num_LH);

                $("input[name='LHrpmOpr']").val(data.LH_rpm_Opr);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_LHrpmOpr']").text(data.LH_rpm_Opr);
                $("input[name='LHrpmNL']").val(data.LH_rpm_NL);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_LHrpmNL']").text(data.LH_rpm_NL);
                $("input[name='LHWattsOpr']").val(data.LH_watts_Opr);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_LHWattsOpr']").text(data.LH_watts_Opr);
                $("input[name='LHPwrTot']").val(data.LH_pwr_tot);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_LHPwrTot']").text(data.LH_pwr_tot);

                $("input[name='LHVOpr']").val(data.LH_V_Opr);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_LHVOpr']").text(data.LH_V_Opr);
                $("input[name='LH_V_NL']").val(data.LH_V_NL);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_LH_V_NL']").text(data.LH_V_NL);


                $("input[name='CableEffTarget']").val(data.cable_eff_target);
                $("input[name='ActualCableEff']").val(data.actual_cable_eff);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_ActualCableEff']").text(data.actual_cable_eff);

                $("input[name='CableLen']").val(data.cable_len);
                $("input[name='LoadVmax']").val(data.Load_Vmax);
                $("input[name='LoadVmin']").val(data.Load_Vmin);
                $("input[name='CableSize']").val(data.cable_size);
                $("input[name='CableAWG']").val(data.cable_AWG);

                $("label[name='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_CableSize']").text(data.cable_mm_title);
                $("label[name='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_CableAWG']").text(data.cable_AWG_title);

                $("input[name='CableA']").val(data.cable_A);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_CableA']").text(data.cable_A);
                $("input[name='Aload_V']").val(data.Aload_V);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_Aload_V']").text(data.Aload_V);
                $("input[name='LoadPwr']").val(data.Load_pwr);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_LoadPwr']").text(data.Load_pwr);

                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_DesignNotesHydro']").text(data.design_notes_hydro);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_DesignNotesElec']").text(data.design_notes_elec);
                $("span[id='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_DesignNotesSafety']").text(data.design_notes_safety);


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

		 function togglePipeFlume(elm) {
			if (elm.val() == "Pipe"){
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeHead']").html('Pipe Fall');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeMat']").html('Pipe Material');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeDia']").html('Pipe Diameter');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeHeight']").html('UNUSED');
				$("#PipeHeight").slideUp();
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeLen']").html('Pipe Length');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_WaterDepth']").html('Water Depth In Pipe');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeCapacity']").html('Pipe capacity');
			} else {
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeHead']").html('Flume Fall');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeMat']").html('Flume Material');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeDia']").html('Flume Width');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeHeight']").html('Flume Height');
				$("#PipeHeight").slideDown();
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeLen']").html('Flume Length');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_WaterDepth']").html('Water Depth In Flume');
				$("label[for='AdvancedCalculatorLHForm_AdvancedCalculatorLHForm_PipeCapacity']").html('Flume capacity');
			};

		}


$(document).ready(function () {
$("#PipeHeight").slideUp();
$("input[name='LoadVmax']").val('400 V');
$("input[name='AvailLPS']").val('20');

inputURL(); //if the user has clicked on the URL in the email which has stored their data this will input it to the form
sendData('firstStart');

			$(".notes .notes").each( function( index, element ){
				$( this ).html($(this).text());
			});


        $("select[name='MeasSys']").on('change',function () {

            setTimeout(function () { sendData('basicdata', $("select[name='MeasSys']")); }, 0);
        });

        $("select[name='Type']").on('change',function () {
            setTimeout(function () { sendData('basicdata', $("select[name='Type']")); }, 0);
        });

        $("input[name='AvailLPS']").on('input',function (event) {

            setTimeout(function () { sendData('basicdata', $("input[name='AvailLPS']")); }, 2000);

        });

         $("input[name='LHHead']").on('input',function (event) {

            setTimeout(function () { sendData('basicdata', $("input[name='AvailLPS']")); }, 2000);

        });

        $("select[name='PipeFlume']").on('change',function () { // this one does somthing special
            togglePipeFlume($("select[name='PipeFlume']"));
        });

        $("input[name='PipeHead']").on('input',function () {
            setTimeout(function () { sendData('basicdata',   $("input[name='PipeHead']")); }, 2000);
        });

        $("select[name='PipeMat']").on('change',function () {
            setTimeout(function () { sendData('basicdata', $("input[name='PipeMat']")); }, 2000);
        });

        $("input[name='PipeDia']").on('input',function () {
            setTimeout(function () { sendData('pipe_dia', $("select[name='PipeDia']")); }, 2000);
        });
        $("input[name='PipeHeight']").on('input',function () {
            setTimeout(function () { sendData('pipe_dia',  $("input[name='PipeHeight']")); }, 2000);
        });
        $("input[name='PipeLen']").on('input',function () {
            setTimeout(function () { sendData('pipelen', $("input[name='PipeLen']")); }, 2000);
        });
        $("input[name='LockNumLH']").on('change',function () {
            setTimeout(function () { sendData('SetLockNumLH',  $("input[name='LockNumLH']")); }, 0);
        });
        $("input[name='NumLH']").on('input',function () {
            setTimeout(function () { sendData('SetNumLH', $("input[name='NumLH']")); }, 2000);
        });




        //electrical
        $("input[name='CableEffTarget']").on('input',function () {
            setTimeout(function () { sendData('SetCableEff',$("input[name='CableEffTarget']")); }, 2000);
        });
        $("input[name='CableLen']").on('input',function () {
            setTimeout(function () { sendData('NewCable',  $("input[name='CableLen']")); }, 2000);
        });
        $("input[name='LoadVmax']").on('input',function () {
            setTimeout(function () { sendData('basicdata',  $("input[name='LoadVmax']")); }, 2000);
        });
        $("input[name='LoadVmin']").on('input',function () {
            setTimeout(function () { sendData('basicdata',  $("input[name='LoadVmin']")); }, 2000);
        });
        $("input[name='CableSize']").on('input',function () {
            setTimeout(function () { sendData('NewCablesize', $("input[name='CableSize']")); }, 2000);
        });
        $("input[name='LockCableSize']").on('change',function () {
            setTimeout(function () { sendData('CableLock',$("input[name='LockCableSize']")); }, 0);
        });
        $("select[name='CableMaterial']").on('change',function () {
            setTimeout(function () { sendData('NewCableMaterial', $("select[name='CableMaterial']")); }, 2000);
        });

        $("input[name='LockCable']").on('change',function () {
            setTimeout(function () { sendData('CableLock',$("input[name='LockCable']")); }, 0);
        });
                $("input[name='CableSize']").on('input',function () {
            setTimeout(function () { sendData('NewCablesize', $("input[name='CableSize']")); }, 2000);
        });
                $("input[name='CableAWG']").on('input',function () {
            setTimeout(function () { sendData('NewCableAWG', $("input[name='CableAWG']")); }, 2000);
        });


        $('#AdvancedCalculatorLHForm_AdvancedCalculatorLHForm').submit(function(e) {


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