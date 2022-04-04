import os
def CreateWifiConfig(SSID, password):
  config_lines = [
    '\n',
    'network={',
    '\tssid="{}"'.format(SSID),
    '\tpsk="{}"'.format(password),
    '\tkey_mgmt=WPA-PSK',
    '}'
  ]

  config = '\n'.join(config_lines)
  print(config)

  with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as f:
    f.write(config)


SSIDd = input("enter  the wifi name")
passwordd = input("enter the wifi name")

CreateWifiConfig(SSIDd, passwordd)