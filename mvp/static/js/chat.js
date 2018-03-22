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
                        '<div class="list-group-item bg-primary pull-right text-right text-white">' + data.date + '<br> '+ data.text + '</div>'+
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
        $.ajax({
            type: "POST",
            url: "sync",
            data: $("#chat-form").serialize(), // serializes the form's elements.
            success: function(data) {
                if(lastMessage != -1 && lastMessage != data.id){
                    lastMessage = data.id;
                    $('#chat-panel').append(
                        '<div class="row">' +
                            '<div class="col"> '+
                                '<div class="list-group-item pull-left">' + data.date + '<br> '+ data.text + '</div>'+
                            '</div>'+
                        '</div>');
                    $('#chat').scrollTop($('#chat')[0].scrollHeight);
                }
            }
        })
    }, 500);
}