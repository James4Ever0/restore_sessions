import launch_on_workspace as low
import os
from check_disk import mount_if_exists, getResult
import requests
import traceback



def checkInternet(url="https://www.baidu.com"):
    try:
        result = requests.get(url, timeout=3)
        status_code = result.status_code
        print("VISIT BAIDU:, status_code")
        return True
    except:
        traceback.print_exc()
        print("NO INTERNET MAYBE.")
    return False

def killAllWithWinName(winName):
    os.system("wmctrl -l | grep %s | xargs -iabc wmctrl -ic abc" % winName)


def checkWindowExists(winName):
    os.system("wmctrl -l | grep %s > output.log" % winName)
    result = getResult()
    if len(result) == 1: return True
    elif len(result)>1:
        killAllWithWinName(winName) # abnormal! will cause all windows to quit.
    return False

# workspace indexs start from zero.
def launchTerminal(directory, command, winName, workspaceId, autoShutdown=False,killPrevious= True):
    if killPrevious:
        killAllWithWinName(winName)
    else:
        if checkWindowExists(winName):
            print("WILL NOT LAUNCH NEW WINDOW FOR %s" % winName)
            return
    # this is to auto shutting down previous instances.
    if autoShutdown: # this will be inconvenient for debugging! if set to default.
        command = 'bash -c "{} ; exit"'.format(command.replace('"', '\\"')) # will not always work.
    wind = low.terminal(workspaceId, directory=directory, command=command, new_win_name=winName)


launchTerminal(
    "/root/Desktop/works/temp-throttle", 'bash temp_throttle.sh 60', "tempThrottle"
,0)
# exit()
# for tujia, maybe you need to check if the disc is missing.
# Disk /dev/sde: 2.73 TiB, 3000592979968 bytes, 5860533164 sectors
# Disk identifier: 0B5A65B7-BC03-452D-8946-1C23088620DA

# lsblk -f: 01D629B7E2676830
result = mount_if_exists("01D629B7E2676830","/media/root/Toshiba3000")
if result:
    launchTerminal("/root/Desktop/works/tujia_beijing_scraping/multi_city_craw","python3 init.py","tujiaCrawler",1)
else:
    print("TOSHIBA 3000 IS NOT ATTACHED")

# for pyjom, ensure the help disk is mounted.
# Disk /dev/sdb: 931.51 GiB, 1000204886016 bytes, 1953525168 sectors
# Disk identifier: 0x01b74ca8
# it is on /dev/sdb2, relatively.

# for lsblk -f we do something else.
# identifier: 46BAFDDFBAFDCB85

result = mount_if_exists("46BAFDDFBAFDCB85","/media/root/help")
if result:
    launchTerminal("/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect","bash launch.sh","qqAutoChat",2)
else:
    print("HELP IS NOT ATTACHED (IMPOSSIBLE?)")
