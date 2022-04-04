import RPi.GPIO as GPIO
import time
import os
from wifi import Cell, Scheme
import subprocess
from stat import S_ISDIR


wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo "


Led_pin1 = 17 #red
Led_pin2 = 27 #blue
Led_pin3 = 22 #green

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO26
GPIO.setup(Led_pin1, GPIO.OUT)  #LED to GPIO17
GPIO.setup(Led_pin2, GPIO.OUT)#led to GPIO27
GPIO.setup(Led_pin3, GPIO.OUT)
GPIO.output(Led_pin2, GPIO.LOW)#intial led2 is low
GPIO.output(Led_pin3, GPIO.LOW)
GPIO.output(Led_pin1, GPIO.LOW)

def btconnect():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Led_pin1, GPIO.OUT)
    GPIO.setup(Led_pin2, GPIO.OUT)
    os.system("rfkill unblock bluetooth")
    os.system("systemctl start bluetooth.service")
    os.system("sudo bluetoothctl discoverable on")    
    os.system("bluetoothctl agent NoInputNoOutput")
    os.system("sudo bluetoothctl agent NoInputNoOutput")
    GPIO.output(Led_pin2, GPIO.HIGH)



def wifi_connect(ssid, psk):
    # write wifi config to file
   
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Led_pin3, GPIO.OUT)
    GPIO.setup(Led_pin1, GPIO.OUT)
    cmd = 'wpa_passphrase {ssid} {psk}  | sudo tee -a {conf} > /dev/null'.format(
            ssid=str(ssid).replace('!', '\!'),
            psk=str(psk).replace('!', '\!'),
            conf=wpa_supplicant_conf
        )
    cmd_result = ""
    cmd_result = os.system(cmd)
    print (cmd + " - " + str(cmd_result))
    # reconfigure wifi
    cmd = sudo_mode + 'wpa_cli -i wlan0 reconfigure'
    #check write or not
    p1= subprocess.Popen(cmd,shell=True)
    p1= subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True).communicate()[0]
    p2=p1.strip()
    if p2 == b'OK' :
        GPIO.output(Led_pin3, GPIO.HIGH)
        GPIO.output(Led_pin1, GPIO.LOW)
    else:
        GPIO.output(Led_pin1, GPIO.HIGH)
    print (cmd + " - " + str(cmd_result))
    time.sleep(10)
    cmd = 'iwconfig wlan0'
    cmd_result = os.system(cmd)
    print("mytest",cmd)
    print (cmd + " - " + str(cmd_result))
    cmd = 'ifconfig wlan0'
    cmd_result = os.system(cmd)
    print (cmd + " - " + str(cmd_result))
    p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = p.communicate()
    if out:
        ip_address = out
        GPIO.output(Led_pin1, GPIO.HIGH)
    else:
        ip_address = "<Not Set>"
        GPIO.output(Led_pin3, GPIO.HIGH)
    return ip_address



try:
    while True:
         button_state = GPIO.input(26)
         if button_state == False:
             GPIO.output(Led_pin2, False)
             print('Bluetooth Button pressed')
             btconnect()
             Ssid = input("enter the name of wifi")
             password = input("enter the password")
             wifi_connect(Ssid,password) 
               
         else:
             GPIO.output(Led_pin1, False)
             

except:
    GPIO.cleanup()