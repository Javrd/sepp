$('#chat').scrollTop($('#chat')[0].scrollHeight);
$("#chat-form").submit(function(e) {

    $.ajax({
        type: "POST",
        url: "",
        data: $("#chat-form").serialize(), // serializes the form's elements.
        success: function(data) {
            $('#chat-panel').append(
                '<div class="row">' +
                    '<div class="col"> '+
                        '<div class="list-group-item bg-primary pull-right text-right text-white">' + $('<div/>').text(data.date).html() + '<br> '+ $('<div/>').text(data.text).html() + '</div>'+
                    '</div>'+
                '</div>');
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
            $('#text').val('');
        }
    });

    e.preventDefault(); // avoid to execute the actual submit of the form.
});

function sync_messages(lastMessage){
    window.setInterval(function (){

        var data = $("#chat-form").serialize();
        data.lastMessageId = lastMessage;
        $.ajax({
            type: "POST",
            url: "sync",
            data: data, // serializes the form's elements.
            success: function(data) {
                data = data.list
                if(lastMessage != -1 && lastMessage != data[data.length-1].id){
                    for (var i=0; i<data.length; i++) {
                        $('#chat-panel').append(
                            '<div class="row">' +
                                '<div class="col"> '+
                                    '<div class="list-group-item pull-left">' + $('<div/>').text(data[i].date).html() + '<br> '+ $('<div/>').text(data[i].text).html() + '</div>'+
                                '</div>'+
                            '</div>');
                        $('#chat').scrollTop($('#chat')[0].scrollHeight);
                        lastMessage = data[i].id;
                        console.log(lastMessage)
                    }
                }
            }
        })
    }, 2000);
}