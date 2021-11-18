from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


@socketio.event
def connect():
    print("\n\n\nCLIENTE CONECTADO COM SUCESSO !\n\n\n")
    emit("client_connect")


@socketio.event
def disconnect():
    print("CLIENTE DESCONECTOU !!!")


# Recebe mensagem que a aplicação FRONT foi iniciada
@socketio.event
def iniciando_front():
    print("\n\n\nAPLICAÇÃO INICIADA\n\n\n")
    emit('carregar_soldagens', broadcast=True)


@socketio.event
def carregar_soldagens():
    print("\n\nSolicitando contagem do Banco de dados\n\n")
    emit('carregar_soldagens', broadcast=True)


# Recebe a contagem do banco de dados
@socketio.event
def contagem_inicial(dados):
    emit('contagem_inicial', dados, broadcast=True)
    print(dados)


@socketio.event
def emit_contagem(cont):
    emit('conta_golpes', cont, broadcast=True)


@socketio.event
def maquina_on(data):
    print("\n\n\n\n MAQUINA LIGADA - FRONT AGUARDANDO CONTAGEM \n\n LIMITE {} \n\n\n\n".format(data))
    emit('maquina_ligada', broadcast=True)
    emit('iniciar_contagem', data, broadcast=True)


@socketio.event
def maquina_off():
    print("\n\n\n\n DESLIGANDO A MAQUINA\n\n\n\n")
    emit('maquina_desligada', broadcast=True)


@socketio.event
def limite_atingido(novo_limite):
    print(f'\n\n ATINGIDO LIMITE DE GOLPES \n{novo_limite}\n\n')
    emit('limite_atingido', broadcast=True)
    emit('limite_extendido', novo_limite, broadcast=True)
    emit('maquina_desligada', broadcast=True)


@socketio.event
def eletrodo_substituido(eletrodo):
    emit('eletrodo_substituido', eletrodo, broadcast=True)


@socketio.on('novo_limite')
def novo_limite(limite):
    print(f'\n\n\n LIMITE \n {limite} \n\n')
    time.sleep(1)
    emit('set_limite', limite, broadcast=True)
    time.sleep(1)
    emit('set_limite', limite, broadcast=True)
    time.sleep(1)
    emit('set_limite', limite, broadcast=True)


@app.route('/', methods=['GET'])
def Retorno():
    return jsonify({"retorno": "ok"})


if __name__ == "__main__":
    socketio.run(app)
