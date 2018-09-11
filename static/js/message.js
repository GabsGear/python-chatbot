
$(".btn-reset").click(function(){
    location.reload();
})

(function () {
    var Message;
    Message = function (arg) {
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        return this;
    };
    $(function () {
        var getMessageText, message_side, sendMessage;
        message_side = 'right';
        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        sendMessage = function (text) {
            var $messages, message;
            if (text.trim() === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
            message_side = message_side === 'left' ? 'right' : 'left';
            message = new Message({
                text: text,
                message_side: message_side
            });
            message.draw();
            return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        };
        $('.send_message').click(function (e) {
            var text = getMessageText()
            sendMessage(getMessageText())
            $.ajax({                
                url: '/send',
                data: {msg_cliente : text},
                type: 'POST',
                success: function(response){sendMessage(response)},
                error:function(error){console.log(error)}
            });
        });
        $('.message_input').keyup(function (e) {
            if (e.which === 13) {
                var text = getMessageText()
                sendMessage(getMessageText())
                $.ajax({                
                    url: '/send',
                    data: {msg_cliente : text},
                    type: 'POST',
                    success: function(response){sendMessage(response)},
                    error:function(error){console.log(error)}
                });
            }
        });
    });
}.call(this));