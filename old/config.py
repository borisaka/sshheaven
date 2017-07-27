import logging
ssh_host = "localhost"
ssh_user = "b"
ssh_password = "EVEqazWSX135"
timeout = 30
hostname = 'bm'
username = ssh_user
vpn_config_path = "/Users/b/.config/vpn.ovpn"
env_path="/usr/bin:/usr/sbin:/bin:/sbin:/usr/local/bin:/usr/local/sbin"
allow_countries = []
reject_countries = ['RU', 'UA', 'KZ']
use_sudo = True 
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
