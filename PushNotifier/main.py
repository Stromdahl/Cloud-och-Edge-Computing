import telegram_send
import paho.mqtt.client as mqtt

mqtt_address = "192.168.1.100"
port = 1883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test")


def on_message(client, userdata, msg):
    message = msg.payload.decode('ascii')
    print(message)
    telegram_send.send(messages=[message])


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_address, 1883, 60)

    client.publish("test", "on")

    client.loop_forever()


if __name__ == '__main__':
    main()
