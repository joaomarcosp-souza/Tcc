$(document).ready(function () {


    // $('.time').mask('00:00:00');
    // $('input[type=date]').mask('00/00/0000');
    $('input[type=datetime]').mask('00/00/0000 00:00:00');

    $('#id_cpf').mask('000.000.000-00');
    $('#id_rg').mask('000.000.000-0', { reverse: true });

    var SPMaskBehavior = function (val) {
        return val.replace(/\D/g, '').length === 11 ? '(00) 0 0000-0000' : '(00) 0000-00009';
    },
        spOptions = {
            onKeyPress: function (val, e, field, options) {
                field.mask(SPMaskBehavior.apply({}, arguments), options);
            }
        };

    $('input[name*=telefone]').mask(SPMaskBehavior, spOptions);
    $('input[name*=cpf]').mask('000.000.000-00');
    $('input[name*=rg]').mask('000.000.000-0', { reverse: true });
    $("input[id*=data]").attr("type", "date");

    $('input[name*=start_time]').attr("type", "date");
    $('input[name*=end_time]').attr("type", "date");

});