import argparse
import logging
import paho.mqtt.client as mqtt
import json


DEFAULT_LOG_LEVEL = 'DEBUG'
DEFAULT_BEACON_MAC = 'C300000A5F41'
DEFAULT_MQTT_SERVER_ADDRESS = 'mqtt5'
DEFAULT_MQTT_USER_NAME = 'admin'
DEFAULT_MQTT_PASSWORD = 'admin'
DEFAULT_MQTT_TOPIC = 'pub'
DEFAULT_MQTT_PORT = 1883
DEFAULT_MQTT_KEEP_ALIVE = 60


def get_args():
    parser = argparse.ArgumentParser(
        description="mqtt-client - i10 Beacon"
    )
    parser.add_argument(
        '--beacon_mac',
        required=False,
        default=DEFAULT_BEACON_MAC,
        type=str,
        help='Beacon MAC address.'
    )
    parser.add_argument(
        '--loglevel',
        default=DEFAULT_LOG_LEVEL,
        choices=['DEBUG', 'WARNING', 'INFO', 'ERROR', 'CRITICAL'],
        help=f'Logging level choices : DEBUG, WARNING, \
               INFO, ERROR, CRITICAL, default={DEFAULT_LOG_LEVEL}'
    )
    parser.add_argument(
        '--mqtt_server_address',
        default=DEFAULT_MQTT_SERVER_ADDRESS,
        required=False,
        type=str,
        help='MQTT server address.'
    )
    parser.add_argument(
        '--mqtt_server_user',
        default=DEFAULT_MQTT_USER_NAME,
        required=False,
        type=str,
        help='MQTT server user name.'
    )
    parser.add_argument(
        '--mqtt_server_password',
        default=DEFAULT_MQTT_PASSWORD,
        required=False,
        type=str,
        help='MQTT server password.'
    )
    parser.add_argument(
        '--mqtt_topic',
        default=DEFAULT_MQTT_TOPIC,
        required=False,
        type=str,
        help='MQTT topic.'
    )
    parser.add_argument(
        '--mqtt_port',
        default=DEFAULT_MQTT_PORT,
        required=False,
        type=int,
        help='MQTT port.'
    )
    parser.add_argument(
        '--mqtt_keep_alive',
        default=DEFAULT_MQTT_KEEP_ALIVE,
        required=False,
        type=int,
        help='MQTT keep alive.'
    )
  
    return parser.parse_args()


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Reason_code_list can have have multiple results if subscribed to multiple
    # topics. We only subscribed to one topic so the array has one element.
    if reason_code_list[0].is_failure:
        logging.debub(f'Subscription rejected. Reason : {reason_code_list[0]}')
    else:
        logging.debug(f'Broker granted the following QoS: {reason_code_list[0].value}')


def on_connect(client, userdata, flags, reason_code, properties):
    if (userdata is not None) and ('topic' in userdata):
        topic = userdata['topic']

        if reason_code.is_failure:
            logging.error(f'Failed to connect: {reason_code}. loop_forever() will retry connection')
        else:
            logging.debug(f'Connected with reason code: {reason_code}')
            logging.debug(f'Subscribed to topic : {topic}')
            client.subscribe(topic)
    else:
        err = 'Topic not passed in as userdata element in connection callback'
        logging.error(err)
        raise Exception(err)


def on_message(client, userdata, msg):
    result = {}

    if (userdata is not None) and ('tag' in userdata):
        tag_to_filter = userdata['tag']
        json_msg = json.loads(str(msg.payload.decode('utf-8')))
        data = json_msg['data'][0]

        if 'tag' in data and data['tag'] == tag_to_filter:
            if 'type' in data and data['type'] == 'EddystoneTLM':
                result['ts'] = data['ts']
                result['gw'] = data['gw']
                result['tag'] = data['tag']
                result['beacon_type'] = 'i10'
                result['vbatt'] = data['vbatt']
                result['temp'] = data['temp']
                logging.debug(f'Beacon data : {result}')
                result = client.publish('i10', json.dumps(result))
    else:
        err = 'Tag not passed in as userdata element in message callback'
        logging.error(err)
        raise Exception(err)


def main():
    args = get_args()
    # Set logging level for script
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=args.loglevel)
    logging.debug(f'Beacon MAC address : {args.beacon_mac}')
    logging.debug(f'MQTT Server address : {args.mqtt_server_address}')
    client_user_data = {
        'topic':args.mqtt_topic,
        'tag': args.beacon_mac
    }
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, userdata=client_user_data)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.username_pw_set(args.mqtt_server_user, args.mqtt_server_password)
    client.connect(args.mqtt_server_address, args.mqtt_port, args.mqtt_keep_alive)
    client.loop_forever()


if __name__ == '__main__':
    main()
