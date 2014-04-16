$(document).ready(function () {
  
  ocultarElementosNoAjax();

  $('#form-seleccion_modalidad').live('submit', function (e) {
    e.preventDefault();
    _get($(this).attr('action'), seleccionModalidadHandler, $(this).serialize());
  });

  $('#form-seleccion_modalidad_mas_info').live('submit', function (e) {
    e.preventDefault();
    _post($(this).attr('action'), $(this).serialize(), seleccionModalidadHandler);
  });

  $('#id_modalidad_disp').live('change', function () {
    $('#form-seleccion_modalidad').submit();
  });

  $('#link-seleccion_modalidad_siguiente').click(function (e) {
    e.preventDefault();
    $('#form-seleccion_modalidad_mas_info').submit();
  });

  $('#id_modalidad_disp option:selected').not('[value=""]').each(function () {
    $('#form-seleccion_modalidad').submit();
  });

  function ocultarElementosNoAjax() {
    $('#id_cat_tipo_inscripcion_licenciatura_0').parent().hide();
    $('#submit-actualizar_licenciaturas').hide();
    $('#submit-seleccion_modalidad_no_ajax').hide();
  }

  function seleccionModalidadHandler(data) {
    if (data.url_redirect) {
      window.location = data.url_redirect
    } else {
      $('#div-seleccion_modalidad').html(data.html);
      ocultarElementosNoAjax();

      var $opcionSeleccionada = $('#id_modalidad_disp option:selected');
      if ($opcionSeleccionada.val() == undefined || $opcionSeleccionada.val() == "" || $('#id_contrato_aceptado').val() != undefined) {
        $('#link-seleccion_modalidad_siguiente').hide();
      } else {
        $('#link-seleccion_modalidad_siguiente').show();
      }
    }
  }

});
