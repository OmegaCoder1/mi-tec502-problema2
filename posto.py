import publisher
from flask import Flask

class Publisher():

    def __init__():
        self.broker    = 'localhost'
        self.port      = 1883
        self.topic     = "fila/posto"
        self.client_id = f'{random.randint(0, 1000)}'

    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Conectado ao Broker MQTT!")
            else:
                print("Falha ao conectar, código de erro: %d\n", rc)
            # Configura o ID do publisher
            client = mqtt_client.Client(client_id)
            client.on_connect = on_connect
            client.connect(broker, port)
            return client

    def publish(client, msg):
        gas_sation_number = 0
        while True:
            time.sleep(5)
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Enviando `{msg}` ao tópico `{topic}`")
            else:
                print(f"Falha ao enviar mensagem ao tópico {topic}")
            gas_sation_number += 1

class Posto(Publisher):

    def __init__(self) -> None:
        self.fila = 0
        self.publisher = publisher.connect_mqtt()

    def aumenta_fila(self) -> None:
        self.fila += 1

    def reduz_fila(self) -> None:
        self.fila -= 1
    

    @posto.route("/")
    def serve_dados_p_server():
        return jsonify(self.publisher.publish(fila))


def main():
    novo_posto = Posto()
    novo_posto.rand


if __name__ == "__main__":
