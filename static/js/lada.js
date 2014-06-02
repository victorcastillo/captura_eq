$(document).ready(function () {

  if ($('#id_lada').val() == '') {
    $('#id_lada').val('Clave');
  }

  $('#id_lada').focusin(function () {
    if ($(this).val() == 'Clave') {
      $(this).val('');
    }
  });

  $('#id_lada').focusout(function () {
    if ($(this).val() == '') {
      $(this).val('Clave');
    }
  });

  $('#form-registro').submit(function () {
    if ($('#id_lada').val() == 'Clave') {
      $('#id_lada').val('')
    }
  });

});
