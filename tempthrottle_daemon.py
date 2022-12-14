import os
import time
cmd = "/bin/bash /root/Desktop/works/temp-throttle/temp_throttle.sh 60"
while True:
    os.system(cmd)
    time.sleep(3)
    print("SOME SHIT HAPPENS. RESTARTING THERMAL THROTTLE")
