$(document).ready(function () {
  $('#registro-link_reset_password').click(function (e) {
    e.preventDefault();
    _get($(this).attr('href'), function (data) {
      $.fancybox(data);
    }); // _get
  }); // click

  $('#reset-submit_password_reset').live('submit', function (e) {
    e.preventDefault();
    _post($(this).attr('action'), $(this).serialize(), function (data) {
      $.fancybox(data);
    }); // _post
  }); // submit

  $('#signin-link').fancybox();
  $('#signin-link').click();
  $('#completar-login-close').click(function () {
    $.fancybox.close();
  })
});
