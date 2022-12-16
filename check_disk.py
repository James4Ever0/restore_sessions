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

def uber_umount(descriptor):
    os.system("umount -l %s" % descriptor)
    os.system("umount -f %s" % descriptor)

def mount_if_exists(device_id, targetDirectory):
    descriptor = check_device_descriptor(device_id)
    print(descriptor)
    if descriptor is not False: # exists!
        # check if mounted to our target directory.
        # check if the target directory is empty, inaccessible.

        os.system("mount | grep %s | grep %s > output.log" % (targetDirectory, descriptor))
        result = getResult()
        if (lr:=len(result)) == 1: # there can only be one.
            # no need for double mount.
            # of course not! maybe it is mounted elsewhere!
            mLog = result[0].split(" ")
            if targetDirectory in mLog:
                try:
                    mfiles = os.listdir(targetDirectory)
                    mflag = len(mfiles)!=0
                    if mflag:
                        print("targetDirectory",targetDirectory,"is empty")
                except:
                    print("fail to listdir for:",targetDirectory)
                    mflag=False
                
                if mflag:
                    return True
        else:
            print("total mounted instances:",lr)
            print("will remount:",targetDirectory)
        # if check failed the unmount the thing and mount the thing again.
        # force to unmount!
        # do not use umount -f alone since it does not work on "lazy" things.
        uber_umount(descriptor)
        uber_umount(targetDirectory)
        if not os.path.exists(targetDirectory):
            os.mkdir(targetDirectory)
        os.system("mount %s %s" % (descriptor, targetDirectory))
    else: 
        print('fail to identify disk for:', targetDirectory)
        return False # false when no such disk was found.
    return True

if __name__ == '__main__':
    device_id = "46BAFDDFBAFDCB85"
    targetDirectory = "/media/root/help"
    result = mount_if_exists(device_id, targetDirectory)
    print("MOUNT RESULT:",result)
