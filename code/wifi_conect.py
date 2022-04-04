import os

def commandExists(command):
    def canExecute(file):
        return os.path.isfile(file) and os.access(file, os.X_OK)
    for path in os.environ["PATH"].split(os.pathsep):
        file = os.path.join(path, command)
        if canExecute(file):
            return True
    return False

if not commandExists("ifconfig"):
    print ("You will need the command 'ifconfig' to continue.")
    quit()
status = os.popen("ifconfig wlan0 up").read()
if 'No such device' in status:
    print ( "It seems your wireless device is not named wlan0, so you're going to need to enter it manually.")
    winame = raw_input('Wireless Device Name: ')
else:
    winame = "wlan0"
print ("Wireless device enabled!")
print ("Checking for available wireless networks...")
stream = os.popen("iwlist " + winame + " scan")
print ("Available Networks:")
networksfound = 0
for line in stream:
    if "ESSID" in line:
        networksfound += 1
        print (" " + line.split('ESSID:"', 1)[1].split('"', 1)[0])
        
        
if networksfound == 0:
    print ("Looks like we didn't find any networks in your area. Exiting...")
    quit()



