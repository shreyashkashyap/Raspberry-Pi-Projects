import subprocess
import time
import argparse

parser = argparse.ArgumentParser(description='Display WLAN signal strength.')
parser.add_argument(dest='interface', nargs='?', default='wlan0',
                    help='wlan interface (default: wlan0)')
args = parser.parse_args()

print ('\n---Press CTRL+Z or CTRL+C to stop.---\n')

while True:
    cmd = subprocess.Popen('iw dev %s link' % args.interface, shell=True,
                           stdout=subprocess.PIPE)
    # print "cmd.stdout",cmd.stdout
    
    for line in cmd.stdout:
        
        if b'signal' in line:
            # print"s"
            s=str(line.lstrip(b' '))
            print (s[4:-3:])
        elif b'Not-Associated' in line:
            print ('No signal')
    time.sleep(1)
