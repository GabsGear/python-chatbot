// Botão para dar refresh na página e assim começar uma nova conversa
$(".btn-reset").click(function(){
    location.reload();
})

/**
 * Função criada com o objetivo de adicionar a 
 * mensagem no chat.
 */

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

    /**
     * Funcão com o objetivo de obter a mensagem, tratar ela
     *  e então encaminhar para a função responsavel por enviar
     *  a mensagem ao chat. 
     * 
     * getMessageText() - Tem como objetivo obter a mensagem do usuário
     * sendMessage() - Tem como objetivo exibir a mensagem no chat.
     */
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

        //Função que enviará as mensagens ao chat quando clicado no botão de Enviar
        $('.send_message').click(function (e) {
            var text = getMessageText()
            sendMessage(getMessageText())
                
            /**
            * Envia a mensagem do usuário via ajax e POST, para que 
            * o servidor possa tratar e enviar essa mensagem para o c
            * hatterbot e assim obter uma resposta.
            */
            $.ajax({                
                url: '/send',
                data: {msg_cliente : text},
                type: 'POST',
                success: function(response){sendMessage(response)},
                error:function(error){console.log(error)}
            });
        });

        //Função que enviará as mensagens ao chat quando presionado o botão ENTER
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