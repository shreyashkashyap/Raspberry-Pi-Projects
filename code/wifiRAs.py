import json


def command_add_wifi(json):
  print("-> Adding wifi")
  
  # Read file WPA suppliant
  networks = []
  with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r") as f:
    in_lines = f.read()  

  # Discover networks
  out_lines = []
  networks = []
  i = 0
  isInside = False
  for line in in_lines:
    if "network={" == line.strip().replace(" ", ""):
      networks.append({})
      isInside = True
    elif "}" == line.strip().replace(" ", ""):
      i += 1
      isInside = False
    elif isInside:      
      key_value = line.strip().split("=")
      networks[i][key_value[0]] = key_value[1]
    else:
      out_lines.append(line)

  # Update password or add new
  isFound = False
  for network in networks:
    if network["ssid"] == f"\"{json['ssid']}\"":
      network["psk"] = f"\"{json['psk']}\""
      isFound = True
      break
  if not isFound:
    networks.append({
      'ssid': f"\"{json['ssid']}\"",
      'psk': f"\"{json['psk']}\"",
      'key_mgmt': "WPA-PSK"
    })

  # Generate new WPA Supplicant
  for network in networks:
    out_lines.append("network={\n")
    for key, value in network.items():
      out_lines.append(f"    {key}={value}\n")      
    out_lines.append("}\n\n")

  # Write to WPA Supplicant
  with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as f:
    for line in out_lines:
      f.write(line)

  print("-> Wifi added !")

json={"ssid": "ZTHub5G", "psk": "58T7KSEEP6"}
print(json)
command_add_wifi(json)