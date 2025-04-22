import csv
from datetime import datetime
from paho.mqtt import client as mqtt
from time import sleep

arquivo = "coleta.csv"
mqtt_broker = 'em.sj.ifsc.edu.br'
mqtt_port = 1883
mqtt_client_id = "tradutor-v0"
mqtt_topic = "em/v0"


if __name__ == "__main__":
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, mqtt_client_id)
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)

    dia = 1
    hoje = datetime.now().strftime("2025 03 " + str(dia))

    arquivo = open(arquivo, "r")
    for linha in arquivo:
        ordem, hora, m2qg, m5qg, m7qg, d18t, bmpp, dhtu, prcp = linha.strip().split(";")
        payload = []
        payload.append(f"m2qg={m2qg}")
        payload.append(f"m5qg={m5qg}")
        payload.append(f"m7qg={m7qg}")
        payload.append(f"d18t={d18t}")
        payload.append(f"bmpp={bmpp}")
        payload.append(f"dhtu={dhtu}")
        payload.append(f"prcp={prcp}")
        payload = ",".join(payload)

        hora, minuto = hora.split(":")
        if hora == "00" and minuto == "00":
            dia += 1
            hoje = datetime.now().strftime("2025 03 " + str(dia))
        hora = datetime.strptime(f"{hoje} {hora}:{minuto}", "%Y %m %d %H:%M")

        payload = " ".join(["EMv0", payload, str(int(hora.timestamp()))])
        print(ordem, payload)
        mqtt_client.publish(mqtt_topic, payload)
        sleep(0.01)
    arquivo.close()

    # mqtt_client.disconnect()
