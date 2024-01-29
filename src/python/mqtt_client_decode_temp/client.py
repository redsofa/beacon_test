import paho.mqtt.client as mqtt
import json
import ast


TAG = 'AC233FAE2EF7'
MQTT_SERVER = 'mqtt5'

# The callback function of connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("pub")


# The callback function for received message
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload.decide('utf-8'))
    json_msg = json.loads(str(msg.payload.decode('utf-8')))
    if json_msg['data'][0]['tag'] == 'AC233FAE2EF7':
        data = json_msg['data'][0]['raw_data']
        timestamp = json_msg['data'][0]['ts']
        print('Timestamp : {}'.format(timestamp))
        print('Raw data : {}'.format(data))

        gen_info = data[0:14]  # general info is the first 7 bytes

        frame_type = data[14:16]
        frame_version = data[16:18]
        if frame_version == '05':  # Temp and humidity frame
            print('Temperature data ...')
            temp_hex = '0x' + data[24:28]
            temp_lit = ast.literal_eval(temp_hex)
            temp = round(temp_lit/256, 1)
            print('Temperature : {t}'.format(t=temp))

            hum_hex = '0x' + data[28:32]
            hum_lit = ast.literal_eval(hum_hex)
            hum = round(hum_lit/256, 1)
            print('Humidity : {h}'.format(h=hum))

        if frame_version == '00':
            print('Battery info ...')
            bat_hex = '0x' + data[30:34]
            bat_lit = ast.literal_eval(bat_hex)
            bat = round(bat_lit/256, 1)
            print('Battery Percent : {}'.format(bat))
        print()
        print()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('admin', 'admin')
client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()
