

from ast import arg
from tracemalloc import stop
import subprocess
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

AllowedActions = ['both', 'publish', 'subscribe']
for_command_id = " "
for_command = ''

success_dict = {

    'command_id' : None,

    'status' : '',

    'description' : ''
    }
error_dict= {

    'command_id' : None,

    'status' : '',

    'description' : ''
    }
stop_dict = {
    'command_id' : None,
    'status' : '',
    'description' : '',
    'start_time' : None,
    'stop_time' : None,
    'power_consumption' : None
}
# Custom MQTT message callback
def customCallback(client, userdata, message):
    
    
    
    print("Received a new message: ")
    print(message.payload)
    
    print("--------------\n\n")
    dirmess=message.payload
    # using decode() + loads()  to convert to dictionary
    res_dict = json.loads(dirmess.decode('utf-8'))
    #res_dict is  in dictornary form
    global for_command_id
    global for_command
    for_command=res_dict.get('command')
    for_command_id=res_dict.get('command_id')
    global start_time
    global stop_time
    global stop_dict
    global success_dict 
    global error_dict
    if for_command in ["START_CHARGING"]:
        start_time = time.time()
        success_dict['command_id'] = for_command_id
        success_dict['status'] = 'Successfully start'
        success_dict['description'] = 'Successfully start the charging'
        time.sleep(3)
        
        
        
    if for_command in ["STOP_CHARGING"]:
        stop_time = time.time()
        stop_dict['command_id'] = for_command_id
        stop_dict['status'] = 'Successfully stop'
        stop_dict['description'] = 'Successfully stop the charging'
        stop_dict['start_time'] = start_time
        stop_dict['stop_time'] = stop_time
        
        time.sleep(3)
        
        
    
    if for_command not in ["STOP_CHARGING" ,"START_CHARGING"]:
        error_dict['command_id'] = for_command_id
        error_dict['status'] = 'ERROR'
        error_dict['description'] = 'something went to be wrong'
        
   


        
    

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="zehnev/iot/zehncp/zehncp-indore-01", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default=" ",
                    help="Message to publish")
parser.add_argument(dest='interface', nargs='?', default='wlan0',
                    help='wlan interface (default: wlan0)')


args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
# if args.mode == 'both' or args.mode == 'subscribe' :
#     myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
#     publish()         
# time.sleep(10)

# Publish to the same topic in a loop forever
loopCount = 0
t=True
while t:
    cmd = subprocess.Popen('iw dev %s link' % args.interface, shell=True,
                           stdout=subprocess.PIPE)
    for line in cmd.stdout:
        if b'signal' in line:
            # print"s"
            siganl_strength=str(line.lstrip(b' '))
        elif b'Not-Associated' in line:
            siganl_strength = 'no network'
            

   
    if args.mode == 'both' or args.mode == 'publish':
        message = {}
        message['message'] = 'SIGNAL_STRENGTH'
        message['message_id'] = for_command_id
        message['signal_strength'] = siganl_strength 
        message['note'] = ''
        message['sequence'] = loopCount
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        if args.mode == 'publish':
            print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1   
        time.sleep(10)
    if args.mode == 'both' or args.mode == 'subscribe' :
        myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
        print('\n ----+----\n')

        if args.mode == 'both' or args.mode == 'publish':
            if for_command in ["START_CHARGING"]:
                message = success_dict
            elif for_command in ["STOP_CHARGING"]:
                message = stop_dict
            else:
                message = error_dict
        
            messageJson = json.dumps(message)
            myAWSIoTMQTTClient.publish(topic, messageJson, 1)
            if args.mode == 'publish':
                print('Published topic %s: %s\n' % (topic, messageJson))
             
        time.sleep(3)






