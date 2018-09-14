# -*- coding: utf-8 -*-
""" 

    Aplicação flask para integração com javascript do chatbot.

    -Função:
        Esse módulo processa o as requisições ajax e cria as rotas para a comunicação do backend 
        (python) com o frontend (javasript).
        
        São criadas duas rotas, a default do index e a roda /send onde são enviadas as respostas
        do bot para a interface.

    -Autores: -Eduardo Vianna
              -Gabriel Estevam
              -Gabriel Ghellere

"""

# Importacao de bibliotecas
from __future__ import print_function

# -Modulos globais:
#  flask 
from flask import Flask, render_template, request
from concurrent import futures
import time

# gprc protocol, da gprcio lib
import grpc

# Modulos chatterbot
import chatterbot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
import os

# -Modulos locais (api grpc)
import helloworld_pb2
import helloworld_pb2_grpc

# instancia a aplicacao no flask
app = Flask(__name__)

# cria a rota index
@app.route('/')

def index():
    """
        Objetivo: Essa funcao renderiza o template default do site, onde são carregadas todas
        as informações estáticas a partir do template client.html localizado na pasta templates.

        Quando executamos esse aplicativo a primeira página renderizada no servidor sera a pagina
        definida na funcao render template (client.html no nosso caso).
    """
    return render_template('client.html')

# cria a rota /send e habilita o metodo POST
@app.route('/send', methods = ['POST'])

def get_post_javascript_data():
    """
        Objetivo: Essa funcao realiza as seguintes operacoes:
            1- Recebe a mensagem do client  por meio de do metodo POST
            2- Chama a rotina do servidor para processar a mensagem recebida
            3- Recebe do servidor uma resposta
            4- Retorna resposta recebida do servidor para o frontend
    """
    # instanciando canal de comunicacao grpc
    with grpc.insecure_channel('localhost:50051') as channel:
        # recebe a mensagem do client por ajax
        msg = request.form['msg_cliente']
        # obtem a resposta do chatbot chamando o servidor e retorna para o frontend
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=msg))
    return str(response.message)

if __name__ == "__main__":

    # Levanta o servidor local e executa a aplicaçao
    app.run(debug=True)

