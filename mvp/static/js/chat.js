$('ul').scrollTop($('ul')[0].scrollHeight);

function loadChat(userId, contactId, proto) {
    var roomName = contactId;

    var chatSocket = new WebSocket(
        proto + '://' + window.location.host +
        '/' + proto + '/chat/' + roomName + '/');

    chatSocket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        var date = data['date'];
        if (data['userId'] == userId) {
            message =
                '<li style="width:100%;">' +
                '<div class="message-r msgWrapper">' +
                '<div class="text text-r">' +
                '<p>' + $('<div/>').text(message).html() + '</p>' +
                '<p style="text-align: left;"><small style="color: black;"><strong>' + $('<div/>').text(date).html() + '</strong></small></p>' +
                '</div>' +
                '<div class="avatar" style="padding:0px 0px 0px 10px !important"><img class="rounded-circle" style="width:100%; margin-top: 5px" src="/media/' + data['image'] + '" /></div>' +
                '</li>';
        } else {
            message =
                '<li style="width:100%">' +
                '<div class="message msgWrapper">' +
                '<div class="avatar"><img class="rounded-circle" style="width:100%; margin-top: 5px" src="/media/' + data['image'] + '" /></div>' +
                '<div class="text text-l">' +
                '<p>' + $('<div/>').text(message).html() + '</p>' +
                '<p style="text-align: left"><small style="color: black;"><strong>' + $('<div/>').text(date).html() + '</strong></small></p>' +
                '</div>' +
                '</div>' +
                '</li>';
        }
        $("ul").append(message).scrollTop($('ul')[0].scrollHeight);
        //$('#chat').scrollTop($('#chat')[0].scrollHeight);
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#text').focus();
    document.querySelector('#text').onkeyup = function (e) {
        if (e.keyCode === 13) { // enter, return
            document.querySelector('#send').click();
        }
        if ($('#text').val().length === 0) {
            $('#pay').removeClass("d-none")
            $('#send').addClass("d-none")
        } else {
            $('#send').removeClass("d-none")
            $('#pay').addClass("d-none")
        }
    };

    document.querySelector('#text').onkeydown = function (e) {
        if ($('#text').val() == '') {
            $('#pay').removeClass("d-none")
            $('#send').addClass("d-none")
        } else {
            $('#send').removeClass("d-none")
            $('#pay').addClass("d-none")
        }
    }

    document.querySelector('#send').onclick = function (e) {
        var messageInputDom = document.querySelector('#text');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));

        messageInputDom.value = '';
        $('#pay').removeClass("d-none")
        $('#send').addClass("d-none")
    };
}