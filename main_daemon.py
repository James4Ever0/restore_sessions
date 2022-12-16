import launch_on_workspace as low
import os
from check_disk import mount_if_exists, getResult
import requests
import traceback

import time
# this is the file being executed in that thing.
from monitor_disks_and_link import threaded

# execute this little helper?
threaded()
os.environ["DISPLAY"] = ":1"

def getProgramWorkingPath(searchList):
    outputPath = 'getProgramWorkingPath.log'
    grepCommand = " | ".join([" grep -i {} ".format(name) for name in searchList])
    executeCommand = "ps aux | "+grepCommand+" | awk '{print $2}' | xargs -iabc pwdx abc | awk '{print $2}' > " +outputPath
    print(executeCommand)
    os.system(executeCommand)
    with open(outputPath, 'r') as f: content = f.read()
    content = [x.strip() for x in content.split("\n")]
    content = [x for x in content if len(x)>3]
    print(content)
    return content

def killProgramWithWorkingPath(searchList, programWorkingPath):
    grepCommand = " | ".join([" grep -i {} ".format(name) for name in searchList])
    executeCommand = "ps aux | "+grepCommand+" | awk '{print $2}' | xargs -iabc pwdx abc | "+"grep {}".format(programWorkingPath)+" | awk -F ':' '{print $1}' | xargs -iabc kill -s KILL abc  " 
    print("KILLING PROGRAM:", searchList, programWorkingPath)
    print(executeCommand)
    os.system(executeCommand)


def checkProgramWorkingPath(searchList, programWorkingPath):
    wps = getProgramWorkingPath(searchList)
    if len(wps) == 0: 
        print("NOT RUNNING:",searchList, programWorkingPath)
        return False
    validPaths =  sum([int(programWorkingPath == x) for x in wps])
    if validPaths == 1:
        print("RUNNING:",searchList, programWorkingPath)
        return True
    else:
        if validPaths >1:
            print("NOT PROPERLY RUNNING:",searchList, programWorkingPath)
            killProgramWithWorkingPath(searchList, programWorkingPath)


def switchToDesktop(index=0, buffer=0.5):
    time.sleep(buffer)
    os.system("wmctrl -s {}".format(index))
    time.sleep(buffer)


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


def checkWindowExists(winName, kill=True):
    os.system("DISPLAY=:1 wmctrl -l | grep %s > output.log" % winName)
    result = getResult()
    if len(result) == 1:
        return True
    elif len(result) > 1:
        #if kill:
        # singleton
        killAllWithWinName(winName)  # abnormal! will cause all windows to quit.
    return False


# workspace indexs start from zero.
def launchTerminal(
    directory, command, winName, workspaceId, sleep=2,autoShutdown=False, relaunch=False
):
    import time
    time.sleep(sleep)
    killPrevious = not relaunch
    if killPrevious:
        killAllWithWinName(winName)
    else:
        if checkWindowExists(winName, kill=not relaunch):
            print("WILL NOT LAUNCH NEW WINDOW FOR %s" % winName)
            return
        killAllWithWinName(winName)
    if workspaceId >= 2 and relaunch == False:
        # time.sleep(1)
        switchToDesktop(index=workspaceId, buffer=1)
        # time.sleep(1) # for gnome to respond properly?
    # this is to auto shutting down previous instances.
    if autoShutdown:  # this will be inconvenient for debugging! if set to default.
        command = 'bash -c "{} ; exit"'.format(
            command.replace('"', '\\"')
        )  # will not always work.
    wind = low.terminal(
        workspaceId, directory=directory, command=command, new_win_name=winName
    )


# def tempThrottle(relaunch=False):
#     launchTerminal(
#         "/root/Desktop/works/temp-throttle", 'bash temp_throttle.sh 60', "tempThrottle"
#     ,0,autoShutdown=True, relaunch=relaunch)
# run tempthrottle as a standalone program.

# exit()
# for tujia, maybe you need to check if the disc is missing.
# Disk /dev/sde: 2.73 TiB, 3000592979968 bytes, 5860533164 sectors
# Disk identifier: 0B5A65B7-BC03-452D-8946-1C23088620DA

# lsblk -f: 01D629B7E2676830

import libtmux


def getRunningTmuxSessionNames():
    try:
        server = libtmux.Server()
        return [x.name for x in server.list_sessions()]
    except:
        return []


def checkTmuxSessionConnected(name):
    try:
        server = libtmux.Server()
        for x in server.list_sessions():
            if x.name == name:
                return x["session_attached"] == "1"
    except:
        return None
    return None


def tujiaScraper(relaunch=True):  # to avoid "NO SUCH DISPLAY" errors.
    # override relaunch flag if no corresponding tmux session running.
    # session prefix: vps_session_unified
    def precondition(relaunch):
        originalRelaunch = relaunch
        relaunch = False
        for name in getRunningTmuxSessionNames():
            if name.startswith("vps_session_unified"):
                # relaunch = originalRelaunch
                print("TUJIA SCRAPER TMUX RUNNING, relaunch flag:", relaunch)
                if not checkTmuxSessionConnected(name):
                    print("REATTACH TUJIA SCRAPER")
                    launchTerminal(
                        "/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect",
                        "tmux attach -t vps_session_unified",
                        "tujiaCrawler",
                        0,
                        relaunch=relaunch,
                    )  # for debugging we should not autoshutdown.
                return
        
        programStatus = checkProgramWorkingPath(["python3","init.py"], "/media/root/Toshiba3000/works/tujia_beijing_scraping")
        if programStatus: return

        killAllWithWinName("tujiaCrawler")
        return True
    result = mount_if_exists("01D629B7E2676830", "/media/root/Toshiba3000")
    if result:
        if precondition(relaunch) == None: return
        launchTerminal(
            "/root/Desktop/works/tujia_beijing_scraping/multi_city_craw",
            "python3 init.py",
            "tujiaCrawler",
            0,
            relaunch=False,
        )
    else:
        print("TOSHIBA 3000 IS NOT ATTACHED")


# for pyjom, ensure the help disk is mounted.
# Disk /dev/sdb: 931.51 GiB, 1000204886016 bytes, 1953525168 sectors
# Disk identifier: 0x01b74ca8
# it is on /dev/sdb2, relatively.

# for lsblk -f we do something else.
# identifier: 46BAFDDFBAFDCB85
def qqAutoChat(relaunch=True):
    def precondition(relaunch):
        print("QQAUTOCHAT MAIN")
        originalRelaunch = relaunch
        relaunch = False
        for name in getRunningTmuxSessionNames():
            print("CHECKING TMUX", name)
            if name == "qq_red_packet":
                # relaunch = originalRelaunch
                # only check if this shit getting connected or not.
                print("QQAUTOCHAT TMUX RUNNING, relaunch flag:", relaunch)
                if not checkTmuxSessionConnected(name):
                    print("SHOWING QQAUTOCHAT")
                    launchTerminal(
                        "/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect",
                        "tmux attach -t qq_red_packet",
                        "qqAutoChat",
                        0,
                        relaunch=relaunch,
                    )  # for debugging we should not autoshutdown.
                return
        
        programStatus = checkProgramWorkingPath(["bash","launch.sh"], "/media/root/parrot/pyjom/tasks/qq/qq_red_packet_collect")
        if programStatus: return
        return True

    if checkInternet():
        parrot_id = "2b809843-2f91-43ea-a4ed-f9f3bbf95a24"
        result = mount_if_exists(parrot_id, "/media/root/parrot")
        # result = mount_if_exists("46BAFDDFBAFDCB85","/media/root/help")
        print("PARROT RESULT:", result)
        if result:
            if precondition(relaunch) == None: return
            print("DECIDE TO RELAUNCH QQAUTOCHAT")
            launchTerminal(
                "/root/Desktop/works/pyjom/tasks/qq/qq_red_packet_collect",
                "bash launch.sh",
                "qqAutoChat",
                0,
                relaunch=False, # forcing relaunch.
            )  # for debugging we should not autoshutdown.
        else:
            print("PARROT IS NOT ATTACHED (IMPOSSIBLE?)")


def classScheduler(relaunch=True):
    # wtf is this relanch=False?
    def precondition(relaunch):
        programStatus = checkProgramWorkingPath(["bash","test.sh"],
            "/root/Desktop/works/course_pass/schedule_alarm")
        if programStatus: return
        return True
    if not precondition(relaunch): return
    launchTerminal(
        "/root/Desktop/works/course_pass/schedule_alarm",
        "bash test.sh",
        "classScheduler",
        0,
        relaunch=False,
    )  # for workspace id >=2, switch to the workspace id first.


# we need to do nothing afterwards but to kee up alive, or systemd will kill everything this process launches.

# really?
# tempThrottle() # this is for joker's

# launch all including those non-permanent ones:

# parrot disk formatted for pyjom: 2b809843-2f91-43ea-a4ed-f9f3bbf95a24
# related services: rclone serve, filesystem watchdogs, filesystem syncdogs, watchdog configs, watchdog init disk mount, qqAutoChat (which is here)
# you need to change the symlink destination of /root/Desktop/works/pyjom

def qqAutoChatNeedRelaunch():
    # check if the lock exists?
    # at least for 30 seconds.
    #import lazero
    import lazero.network.checker
    maxtime = 15
    timeout = 1
    port, message = 8932,{"response": "DFAFilter based Chinese text filter(censor)"}
    # textfilter, one component of our chatbot.
    flag = lazero.network.checker.waitForServerUp(port, message, timeout=timeout,maxtime=maxtime)
    relaunch = not flag
    if relaunch:
        print("qq chatbot need relaunch!")
        os.system("tmux kill-session -t qq_red_packet")
    return relaunch

while True:
    try:
        # disable tujiaScraper
        # tujiaScraper() 
        qqAutoChat(relaunch=qqAutoChatNeedRelaunch())
        classScheduler()
        # switch to workspace id:2 from now? leave all other desktops to run our tasks.
        switchToDesktop(index=1, buffer=1)
        print("SUCCESSFULLY LAUNCHED ALL PROGRAMS.")
        break
    except:
        import traceback

        traceback.print_exc()
        time.sleep(3)
        print("SOME SHIT HAPPENS")


def tryPass(function):
    try:
        function()
    except:
        import traceback

        traceback.print_exc()
        print("ERROR IN TRYPASS EXECUTING %s" % function.__name__)


while True:
    # check tempthrottle. do not exit or computer will blow.
    # tempThrottle(relaunch=True)
    #tujiaCompletedFlag = "/root/Desktop/works/tujia_beijing_scraping/export_beijing_xlsx/suzhou_processed.flag"
    # do not check the tujia crawler since we don't give a shit to that.
    #if not os.path.exists(tujiaCompletedFlag):
    #    tryPass(lambda:tujiaScraper(relaunch=True))
    # disable tujiaScraper.
    # check our qq bot instead. if not running and have internet then we must relaunch that.
    tryPass(lambda: qqAutoChat(relaunch=qqAutoChatNeedRelaunch()))
    tryPass(lambda: classScheduler(relaunch=True))

    time.sleep(5)

    print("SEE IF SYSTEMD IS THE PROBLEM")
    # print("PROGRAM WILL EXIT ON DEMAND.")

# yes it is the problem. and it is a serious one.
