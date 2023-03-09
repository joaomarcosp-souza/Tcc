$(document).ready(function () {
    $("#btn-ver-senha").click(function (e) {
        e.preventDefault();
        var type = $("#id_password").attr("type");
        if (type == "password")
            $("#id_password").attr("type", "text");
        else
            $("#id_password").attr("type", "password");
    });
});


setTimeout(function () {
    $('#alerttimeout').fadeOut('fast');
}, 5000);


setTimeout(function () {
    $('#errologin').fadeOut('fast');
}, 6000);
