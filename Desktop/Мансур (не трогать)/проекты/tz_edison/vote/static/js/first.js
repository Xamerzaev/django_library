$(document).ready(function () {

    var now = new Date();
    var hour = now.getHours();

    for (var i = 0; i < 24; i++) {
        if (i == hour) {
            $("#id_time").val(i);
        }
        else if (i < hour) {
            $("#id_time option[value='" + i + "']").hide();
        }
    }

    $(function () {
        $("#id_event").autocomplete({
            source: "/get_event/",
            select: function (event, ui) {
                AutoCompleteSelectHandler(event, ui)
            },
            minLength: 2
        });
    });

    function AutoCompleteSelectHandler(event, ui) {
        var selectedObj = ui.item;
    }

    var socket = new WebSocket("ws://" + window.location.host + "/vote/");
    socket.onmessage = function (e) {

        if (e.data.substring(0, 5) == 'reset') {
            window.location.replace(location.href.replace('/polls/first/', '/polls/reset/' + e.data.substring(5)));
        }

        $("#votes").text(e.data);

    };
    socket.onopen = function () {

        socket.send($("#vot").val());
    };
    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();

    var socketStart = new WebSocket("ws://" + window.location.host + "/start/");
    if (socketStart.readyState == WebSocket.OPEN) socketStart.onopen();

});