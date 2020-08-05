$.AMUI.progress.start();

$(window).on("load", function () {
    $.AMUI.progress.done();
})

var hideFlash = function () {
    $(".am-alert").fadeOut("slow");
}
setTimeout(hideFlash, 4000);