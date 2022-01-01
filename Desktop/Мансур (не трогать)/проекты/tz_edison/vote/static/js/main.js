$(document).ready(function () {

    var socketStart = new WebSocket("ws://" + window.location.host + "/start/");
    socketStart.onmessage = function (e) {
        window.location.replace(location.href.replace('/polls/', '/polls/first/'));

    };

});