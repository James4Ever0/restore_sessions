# write something for our dynamic monitoring.
# just to make sure it is always mounted at the spot.
# unmount things if not working properly.
# you can launch this before the tujia service.
import time
from check_disk import mount_if_exists
import threading

# no external power chord attached to our xhci device, so frequently facing disk detaching issue.
# myth busted?
# still checking.
def mainlogic():
    info_list = [
        ["01D629B7E2676830", "/media/root/Toshiba3000"],
        ["46BAFDDFBAFDCB85", "/media/root/help"],
        ["2b809843-2f91-43ea-a4ed-f9f3bbf95a24", "/media/root/parrot"],
        ["0009AC2F000F921E", "/media/root/Seagate1000"],# this shit does not work. why the fuck?
    ]

    sleep = 2
    while True:
        for info in info_list:
            # repeatly doing mounting checks.
            try:
                mount_if_exists(*info)
            except:
                import traceback

                traceback.print_exc()
                print("error when mounting {} to {}".format(*info))
        time.sleep(sleep)


def threaded():
    thread = threading.Thread(target=mainlogic, daemon=True)
    thread.start()
