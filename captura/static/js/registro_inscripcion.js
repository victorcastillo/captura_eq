$(document).ready(function () {

  $('#link-mostrar_reglamento').click(function () {
    _get($(this).attr('href'), function (data) {
      $.fancybox({content: data});
    }); // _get
    
    return false;
  });

});

