from __future__ import print_function
from flask import Flask, render_template, request
from concurrent import futures
import time
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import chatterbot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
import os
import sys
import re
import json

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('client.html')

@app.route('/send', methods = ['POST'])
def get_post_javascript_data():
    with grpc.insecure_channel('localhost:50051') as channel:
        msg = request.form['msg_cliente']
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=msg))
    return str(response.message)

if __name__ == "__main__":
    app.run(debug=True)

