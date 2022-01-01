$(document).ready(function () {

    var socket = new WebSocket("ws://" + window.location.host + "/vote/");

    socket.onopen = function () {

        if ($("#active").val() == 'True' && $("#user").val() == 'True') {

            socket.send('reset' + $("#poll_id").val());
        }
    };
    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();

});