import shutil
import spur
shell = spur.SshShell(hostname='localhost', username='fin')
need_sudo = True
# update_path = "PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin"
def correct_args(sh_args):
    if need_sudo:
        sh_args = append_sudo(sh_args)
    # sh_args = [update_path] + sh_args
    return sh_args

def run(sh_args):
    return shell.run(correct_args(sh_args))

def spawn(sh_args):
    return shell.spawn(correct_args(sh_args), store_pid=True)

def kill(pid):
    return run(correct_args(['kill', str(pid)]))

def upload_files(local_path, remote_path):
    with open(local_path, 'rb') as local:
        with shell.open(remote_path, 'wb') as remote:
           return shutil.copyfileobj(local, remote)

def download_files(remote_path, local_path):
    with shell.open(remote_path, 'rb') as remote:
        with open(local_path, 'wb') as local:
           return shutil.copyfileobj(remote, local)

def append_sudo(sh_args):
    if 'sudo' not in sh_args:
        return ['sudo'] + sh_args
    return sh_args

