$(document).ready(function () {

  $('#id_modalidad option:selected').not('[value=""]').each(function () {
    if ($('#id_interesado_en1').val() == '')
      obtener_modalidad(this);
  });

  $('#id_modalidad').change(function () {
    obtener_modalidad(this);
  });

  function obtener_modalidad (thisSelect) {
    var $thisSelect = $(thisSelect);
    var value = $thisSelect.val();

    if (value != '') {
      $.fancybox.showActivity();
      $.get('/registro/obtener-modalidad/'+ value +'/', function (data, textStatus, jqXHR) {
        $.fancybox.hideActivity();
        if (textStatus == 'success') {
          var style = $('#id_interesado_en1').attr('style');
          $('#id_interesado_en1').replaceWith(data.respuesta);
          $('#id_interesado_en1').attr('style', style);
        }
      }); // $.get(..
    }
  }

});
