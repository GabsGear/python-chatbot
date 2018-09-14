# -*- coding: utf-8 -*-
""" 
    Servidor grpc e integracao com chatterbot.

    -Função:
        Nesse modulo é treinado o chatbot e integrado com a api chatterbot e feita toda a comunicação grpc

    -Autores: -Eduardo Vianna
              -Gabriel Estevam
              -Gabriel Ghellere

"""

# Modulos GLobais
from concurrent import futures
import time
import os

# GRPC
import grpc

# Chatterbot
import chatterbot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot

# Modulos locais
import helloworld_pb2
import helloworld_pb2_grpc

# instanciado periodo diario
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# instancia um novo bot do modulo chatterbot
bot = ChatBot("MitoBot")

"""
    Seleciona o tipo de treinamento do chatterbot, no nosso caso usamos um dataset treinado entao 
    para treino online executamos ChatterBotCorpusTrainer no parametro set_trainer
"""
bot.set_trainer(ChatterBotCorpusTrainer)

""" 
    Seleciona o dataset de treino corpus, eh um dataset open sourse disponivel em https://github.com/gunthercox/chatterbot-corpus
    Apos treinada a rede eh criado um banco de dados sqlite no path para que nao seje necessário retreino a cada novo uso
"""
bot.train(
    "chatterbot.corpus.portuguese"
)

class Chatbot():

    def getResponse(self, message): 
        """
            Objetivo: Essa funcao recebe como argumento uma mensagem aleatória e retorna a resposta 
            do bot. A mensagem enviada é selecionada pelo "match" da rede treinada que fica armazenado 
            no arquivo db.sqlite3 criado no treinamento
        """
        return str(bot.get_response(message.name))

class Greeter(helloworld_pb2_grpc.GreeterServicer):
    """
        A classe Greeter eh criada ultilizando heranca da classe GreeterServicer para assim poder utilizar as funcoes ja criadas da api
    """
    def SayHello(self, request, context):

        # cria um objeto da classe chatbot
        response = Chatbot()
        # obtem a resposta do bot chamando getResponse
        response = response.getResponse(request)
        # retorna a mensagem no padrao grpc
        return helloworld_pb2.HelloReply(message=response)


def serve():
    """
        OBjetivo: Cria o servidor de comunicacao grpc na porta 50051
    """

    #define o maximo de threads na pool no caso 10
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # linka o servidor a classe gretter
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    # define a porta para conexao com o client
    server.add_insecure_port('[::]:50051')
    #inicia o server
    server.start()
    
    # Recuperacao de erro
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
