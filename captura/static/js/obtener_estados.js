$(document).ready(function () {

  // ================ ON STARTUP
  $('#id_educacion_ant-pais option:selected').not('[value=""]').each(function () {
    if ($('#id_educacion_ant-estado').val() == '')
      obtener_estados(this, '#id_educacion_ant-estado');
  });

  $('#id_datos_lab-pais option:selected').not('[value=""]').each(function () {
    if ($('#id_datos_lab-estado').val() == '')
      obtener_estados(this, '#id_datos_lab-estado');
  });

  $('#id_pais option:selected').not('[value=""]').each(function () {
    if ($('#id_estado').val() == '')
      obtener_estados(this, '#id_estado');
  });


  // ================ ON CHANGE
  $('#id_educacion_ant-pais').change(function () {
    obtener_estados(this, '#id_educacion_ant-estado');
  });

  $('#id_datos_lab-pais').change(function () {
    obtener_estados(this, '#id_datos_lab-estado');
  });

  $('#id_pais').change(function () {
    obtener_estados(this, '#id_estado');
  });
  
  function obtener_estados(thisSelect, thatSelect) {
    $thisSelect = $(thisSelect);
    var value = $thisSelect.val();

    if (value != '') {
      $.fancybox.showActivity();
      $.get('/registro/obtener-estados/'+ value +'/', function (data, textStatus, jqXHR) {
        $.fancybox.hideActivity();
        if (textStatus == 'success') {
          $(thatSelect).html('');
          for (var id in data) {
            $(thatSelect).append('<option value="' + id + '">' + data[id] + '</option>');
          }
        }
      }); // $.get(..
    } // if(value != ...
  } // function obtener_estados(...

});
