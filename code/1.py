import os
from stat import S_ISDIR
import RPi.GPIO as GPIO
from wifi import Cell, Scheme
import subprocess
import time

wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo "
Led_pin1 = 17 #red
Led_pin2 = 27 #blue
Led_pin3 = 22 #green



GPIO.setmode(GPIO.BCM)
GPIO.setup(Led_pin1, GPIO.OUT)  #LED to GPIO17
GPIO.setup(Led_pin2, GPIO.OUT)#led to GPIO27
GPIO.setup(Led_pin3, GPIO.OUT)
GPIO.output(Led_pin2, GPIO.HIGH)
GPIO.output(Led_pin3, GPIO.LOW)
GPIO.output(Led_pin1, GPIO.LOW)
def wifi_connect(ssid, psk):
    # write wifi config to file
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Led_pin1, GPIO.OUT)  #LED to GPIO17
    GPIO.setup(Led_pin3, GPIO.OUT)
    cmd = 'wpa_passphrase {ssid} {psk}  | sudo tee -a {conf} > /dev/null'.format(
            ssid=str(ssid).replace('!', '\!'),
            psk=str(psk).replace('!', '\!'),
            conf=wpa_supplicant_conf
        )
    cmd_result = ""
    
    cmd_result = os.system(cmd)
    #print (cmd + " - " + str(cmd_result))
    
    # reconfigure wifi
    cmd = sudo_mode + 'wpa_cli -i wlan0 reconfigure'
   
    #cmd_result = os.system(cmd)
    p1= subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True).communicate()[0]
    p2=p1.strip()
    if p2 == b'FAIL' :
        print("led red on")
    else:
        print("green")
    
    
        
    
    #print (cmd + " - " + str(cmd_result))
    time.sleep(10)
    cmd = 'iwconfig wlan0'
    cmd_result = os.system(cmd)
   # print (cmd + " - " + str(cmd_result))
    cmd = 'ifconfig wlan0'
    cmd_result = os.system(cmd)
    #print (cmd + " - " + str(cmd_result))
    p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = p.communicate()
    if out:
        ip_address = out     
    else:
        ip_address = "<Not Set>"
        
    return ip_address

def ssid_discovered():
    Cells = Cell.all('wlan0')
    wifi_info = 'Found ssid : \n'
    for current in range(len(Cells)):
        wifi_info +=  Cells[current].ssid + "\n"
    wifi_info+="!"
    print (wifi_info)
    return wifi_info

Ssid = input("enter the name of wifi")
password = input("enter the password")

if Ssid == "":
    print("plese enter the name")
else:
    wifi_connect(Ssid,password)