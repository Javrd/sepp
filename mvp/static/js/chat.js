$('#chat').scrollTop($('#chat')[0].scrollHeight);
function loadChat (userId, contactId, proto){
    var roomName = contactId;

    var chatSocket = new WebSocket(
        proto + '://' + window.location.host +
        '/'+ proto +'/chat/' + roomName + '/');
        
    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        var date = data['date'];
        if  (data['userId'] ==  userId) {
            $('#chat-panel').append(
                '<div class="row">' +
                    '<div class="col"> '+
                        '<div class="list-group-item bg-primary pull-right text-right text-white">' + $('<div/>').text(date).html() + '<br> '+ $('<div/>').text(message).html() + '</div>'+
                    '</div>'+
                '</div>');
        } else {
            $('#chat-panel').append(
                '<div class="row">' +
                    '<div class="col"> '+
                        '<div class="list-group-item pull-left">' + $('<div/>').text(date).html() + '<br> '+ $('<div/>').text(message).html() + '</div>'+
                    '</div>'+
                '</div>');
        }
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#text').focus();
    document.querySelector('#text').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#send').click();
        }
    };

    document.querySelector('#send').onclick = function(e) {
        var messageInputDom = document.querySelector('#text');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));

        messageInputDom.value = '';
    };
}