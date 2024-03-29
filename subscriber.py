from paho.mqtt import client as mqtt_client
import random
import time
from flask import Flask
from flask import jsonify
broker = 'localhost'
port = 1883
topic = "fila/posto"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# cache armazenando todas as filas de todos os postos
gas_station_queues = []
available_gas_stations = []

app = Flask(__name__)
@app.route("/", methods=("GET", "POST"))
def serve_dados_publicados():
    return jsonify(publish(client))

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT!")
        else:
            print("Erro na conexão, código %d\n", rc)
    # Configura o ID do cliente(subscriber)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
    
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"`{msg.payload.decode()}` Recebida do tópico `{msg.topic}`")
        manage_subscriptions(msg)
    client.subscribe(topic)
    client.on_message = on_message

def manage_subscriptions(msg):
    received_msg = str(msg.payload.decode())
    payload = {}
    payload['id_station'] = received_msg.split('=')[0].split('posto')[1].strip()
    payload['queue_size'] = received_msg.split('=')[1].strip()

    if len(gas_station_queues) == 0:
        gas_station_queues.append(payload)
        available_gas_stations.append(payload['id_station'])
        print('available')
        print(available_gas_stations)
    
    else:
        # if available_gas_stations.index(payload['id_station']) is not None
        if payload['id_station'] in available_gas_stations:
            payload_index = available_gas_stations.index(payload['id_station'])
            gas_station_queues[payload_index]['queue_size'] = payload['queue_size']
        else:
            gas_station_queues.append(payload)    
            available_gas_stations.append(payload['id_station'])
        # for station in gas_station_queues:
        #     if gas_station_info['id_station'] in station['id_station']:
        #         station['queue_size'] = gas_station_info['queue_size']
        #     else:
        #         gas_station_queues.append(gas_station_info)
        
    print(gas_station_queues)

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    app.run(host='localhost', port='12345')

if __name__ == "__main__":
    run()