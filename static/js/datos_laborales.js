$(document).ready(function () {

  var checkedRadio = $('input:radio[name="datos_lab-trabaja_actualmente"]:checked');
  if (checkedRadio.val() == undefined || checkedRadio.val() == 0) {
    $('#datos_laborales_dependientes').hide('fast');
  } else if (checkedRadio.val() == 1) {
    if ($('#id_datos_lab-lada').val() == '') {
      $('#id_datos_lab-lada').val('Clave');
    }
  }

  $('#id_datos_lab-lada').focusin(function () {
    if ($(this).val() == 'Clave') {
      $(this).val('');
    }
  });

  $('#id_datos_lab-lada').focusout(function () {
    if ($(this).val() == '') {
      $(this).val('Clave');
    }
  });

  $('input:radio[name="datos_lab-trabaja_actualmente"]').change(function () {
    if ($(this).val() == 0) {
      $('#datos_laborales_dependientes').hide('fast', function() {
        $('#id_datos_lab-lada').val('');
      });
    } else {
      $('#datos_laborales_dependientes').show('fast', function() {
        $('#id_datos_lab-lada').val('Clave');
      });
    }
  });

  $('#form-datosextra').submit(function () {
    if ($('#id_datos_lab-lada').val() == 'Clave') {
      $('#id_datos_lab-lada').val('')
    }
  });

});

