import os
def getResult():
    with open("output.log","r") as f:
        result =f.read().split("\n")
        result = [x for x in result if len(x)>0]
        print(result) # select first one?
    return result

def check_device_descriptor(device_id):
    command = r'lsblk -f | grep "'+device_id+'"'+r" | awk '{print $1}' | grep -o '\w\+' > output.log"
    print(command)
    os.system(command)
    result = getResult()
    if len(result) ==1:
        return "/dev/{}".format(result[0])
    else:
        return False

def mount_if_exists(device_id, targetDirectory):
    descriptor = check_device_descriptor(device_id)
    print(descriptor)
    if descriptor is not False:
        # check if mounted to our target directory.
        os.system("mount | grep %s | grep %s > output.log" % (targetDirectory, descriptor))
        result = getResult()
        if len(result) == 1:
            # no need for double mount.
            # of course not! maybe it is mounted elsewhere!
            mLog = result[0].split(" ")
            if targetDirectory in mLog:
                return True 
        # if check failed the unmount the thing and mount the thing again.
        # force to unmount!
        os.system("umount -f %s" % descriptor)
        os.system("umount -f %s" % targetDirectory)
        if not os.path.exists(targetDirectory):
            os.mkdir(targetDirectory)
        os.system("mount %s %s" % (descriptor, targetDirectory))
    else: return False
    return True

if __name__ == '__main__':
    device_id = "46BAFDDFBAFDCB85"
    targetDirectory = "/media/root/help"
    result = mount_if_exists(device_id, targetDirectory)
    print("MOUNT RESULT:",result)
