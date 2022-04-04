import bluetooth,subprocess
import json
def show_bluetooth_device():
    nearby_devices = bluetooth.discover_devices(lookup_names = True, flush_cache = True, duration = 20)
    for addr, name in nearby_devices:
        print(f"List of nearby bluetooth device {name}")
def connect_bluetooth():
    target_name = input("Enter bluetooth name :")
    passkey = input("Enter the passcode :")
    target_address =None
    port = 1
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        if target_name == bluetooth.lookup_name( bdaddr ):
            target_address = bdaddr
            break
    subprocess.call("kill -9 `pidof bluetooth-agent`",shell=True)
    status = subprocess.call("bluetooth-agent " + passkey + " &",shell=True)
    try:
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        if s.connect((target_address,port)):
            print("connected successfully")
    except bluetooth.btcommon.BluetoothError as err:
        print(err)
    wifi_id = input("Enter the wifi id :")
    password = input("Enter the password :")
    wifi_cred = {"wifi_id":wifi_id,"password":password}
    wifi_cred = json.dumps(wifi_cred)
    s.send(wifi_cred)
    print("sent wifi credentials")
show_bluetooth_device()
connect_bluetooth()