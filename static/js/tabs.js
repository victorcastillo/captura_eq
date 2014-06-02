$(document).ready(function () {
  var current_tab = $('ul[id^="tabs_menu"]').attr('current_tab');

  if (current_tab != undefined) {
    $('ul[id^="tabs_menu"] li').each(function () {
      var $thisLi = $(this);
      $('a', this).each(function () {
        if ($(this).attr('href') == current_tab) {
          $thisLi.addClass('selected');
          $(this).attr('href', '#');
        }
      }); // $('a', this).each(...
    }); // $('#tabs_menu li').each(...
  }

});
