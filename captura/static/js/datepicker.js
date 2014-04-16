$(document).ready(function () {

  var propiedades = {
    dateFormat: 'mm-yy',  
    constrainInput: true,
    changeMonth: true,
    changeYear: true,
    yearRange: '1960:' + obtener_fecha(0).getFullYear(),
    monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
    dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','S&aacute;'],
    onChangeMonthYear: function (year, month, inst) {
      $(this).val((month < 10 ? '0' + month : month) + '-' + year);
    },
  };

  propiedades.minDate = obtener_fecha(-80);
  propiedades.maxDate = obtener_fecha(0);
  $("#id_educacion_ant-fecha_inicio").datepicker(
    propiedades
  );

  propiedades.minDate = obtener_fecha(-80);
  propiedades.maxDate = obtener_fecha(200);
  $("#id_educacion_ant-fecha_fin").datepicker(
    propiedades
  );

  $("#datepicker").datepicker();

  function obtener_fecha (offset) {
    var fecha = new Date();
    fecha.setFullYear(fecha.getFullYear() + offset);
    fecha.setMonth(11);

    return fecha;
  }

});
