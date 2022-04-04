import urllib
try:
    url = "https://www.google.com"
    urllib.urlopen(url)
    status = "Connected"
except:
    status = "Not connected"
print (status)
if status == "Connected":
    print("Connected")
    # do stuff...