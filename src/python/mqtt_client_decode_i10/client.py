import argparse
import logging
import paho.mqtt.client as mqtt
import json


DEFAULT_LOG_LEVEL = 'DEBUG'
DEFAULT_BEACON_MAC = 'C300000A5F41'
DEFAULT_MQTT_SERVER_ADDRESS = 'mqtt5'
DEFAULT_MQTT_USER_NAME = 'admin'
DEFAULT_MQTT_PASSWORD = 'admin'
DEFAULT_MQTT_OUTPUT_TOPIC = 'i10'
DEFAULT_MQTT_INPUT_TOPIC = 'pub'
DEFAULT_MQTT_PORT = 1883
DEFAULT_MQTT_KEEP_ALIVE = 60
DEFAULT_I10_TOPIC = 'i10'


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
        '--mqtt_input_topic',
        default=DEFAULT_MQTT_INPUT_TOPIC,
        required=False,
        type=str,
        help='MQTT input topic.'
    )
    parser.add_argument(
        '--mqtt_output_topic',
        default=DEFAULT_MQTT_OUTPUT_TOPIC,
        required=False,
        type=str,
        help='MQTT output topic.'
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
    if (userdata is not None) and ('input_topic' in userdata):
        input_topic = userdata['input_topic']

        if reason_code.is_failure:
            logging.error(f'Failed to connect: {reason_code}. loop_forever() will retry connection')
        else:
            logging.debug(f'Connected with reason code: {reason_code}')
            logging.debug(f'Subscribed to topic : {input_topic}')
            client.subscribe(input_topic)
    else:
        err = 'Topic not passed in as userdata element in connection callback'
        logging.error(err)
        raise Exception(err)


def on_message(client, userdata, msg):
    result = {}

    def update_minute_counter(userdata, ts):
        if userdata['counter_start_time'] is None:
            userdata['counter_start_time'] = ts
            userdata['per_min_counter'] = userdata['per_min_counter'] + 1
        else:
            if ts - userdata['counter_start_time'] >= 60:
                userdata['msg_count_for_min'] = userdata['per_min_counter']
                userdata['counter_start_time'] = ts
                userdata['current_minute'] = userdata['current_minute'] + 1
                userdata['per_min_counter'] = 0
            else:
                userdata['per_min_counter'] = userdata['per_min_counter'] + 1

    if (userdata is not None) and ('tag' in userdata):
        tag_to_filter = userdata['tag']
        output_topic = userdata['output_topic']
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
                update_minute_counter(userdata, data['ts'])
                result['per_min_counter'] = userdata['per_min_counter']
                result['msg_count_for_min'] = userdata['msg_count_for_min']
                result['current_minute'] = userdata['current_minute']
                logging.debug(f'Sending beacon data : {result} to output topic : {output_topic}')
                result = client.publish(output_topic, json.dumps(result))
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
        'input_topic': args.mqtt_input_topic,
        'output_topic': args.mqtt_output_topic,
        'tag': args.beacon_mac,
        'per_min_counter' : 0,
        'counter_start_time' : None,
        'msg_count_for_min': 0,
        'current_minute' : 0,
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
