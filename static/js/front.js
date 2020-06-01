$(function () {
    lightbox.option({
      'resizeDuration': 200,
      'wrapAround': true
  });

  /* ===============================================================
         HUMBERGUR MENU ACTIVATE
      =============================================================== */
    $('.navbar-toggler').on('click dblclick', function () {
        $(this).toggleClass('active');
    });
});
