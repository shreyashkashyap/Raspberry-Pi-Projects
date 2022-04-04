import subprocess
cmd = "git branch | grep '*' | cut -d ' ' -f2"
output = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True).communicate()[0]
print(output.strip()) # For single line output.

# For long output.
import subprocess
import tempfile
cmd = "git branch | grep '*' | cut -d ' ' -f2"
with tempfile.TemporaryFile() as tempf:
    proc = subprocess.Popen(cmd, stdout=tempf,shell=True)
    proc.wait()
    tempf.seek(0)
    print(tempf.read())