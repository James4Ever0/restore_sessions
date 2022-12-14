from check_disk import mount_if_exists
parrot_id = "2b809843-2f91-43ea-a4ed-f9f3bbf95a24"
result = mount_if_exists(parrot_id,"/media/root/parrot")
#result = mount_if_exists("46BAFDDFBAFDCB85","/media/root/help")
#result = mount_if_exists("46BAFDDFBAFDCB85","/media/root/help")

import os

cmd = "rclone serve webdav /media/root/parrot/pyjom --addr 0.0.0.0:8468 --key /root/.local/share/code-server/localhost.key --cert /root/.local/share/code-server/localhost.crt --htpasswd /root/Desktop/works/sync_git_repos/remote_deploys/webdav_htpasswd -L"
os.system(cmd)
