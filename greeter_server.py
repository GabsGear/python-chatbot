from concurrent import futures
import time

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


import chatterbot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
import os

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

bot = ChatBot("MitoBot")
bot.set_trainer(ChatterBotCorpusTrainer)

bot.train(
    "chatterbot.corpus.portuguese"
)

class Chatbot():

    def getResponse(self, message):
        ## tem que transformar isso em string
        return str(bot.get_response(message.name))

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        response = Chatbot()
        response = response.getResponse(request)
        return helloworld_pb2.HelloReply(message=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
