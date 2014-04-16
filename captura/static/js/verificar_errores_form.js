$(document).ready(function () {

  var errores = 0;
  $('.errorlist').each(function () {
    errores++;
  });

  if (errores > 0) {
    $.fancybox.showActivity();
    $.get('/registro/formularios/errores/', function (data, textStatus, jqXHR) {
      $.fancybox.hideActivity();
      if (textStatus == 'success' && data.respuesta) {
        for (var i = 0; i < data.respuesta.length; i++) {
          $('#id_' + data.respuesta[i]).css({'background-color': '#e76565', 'color': '#FFFFFF'})
        }
      }
    });

    $.fancybox.showActivity();
    $.get('/registro/modales/completa_datos/', function (data, textStatus, jqXHR) {
      $.fancybox.hideActivity();
      if (textStatus == 'success') {
        $.fancybox({content: data.respuesta});
      }
    });
  }

});
