import re
import sys
import os
import platform
import subprocess

from st2common.util.shell import quote_unix

def get_linux_distribution():
    if hasattr(platform, "linux_distribution"):
        distro = platform.linux_distribution()[0]
    else:
        result = subprocess.run(
            "lsb_release -i -s", shell=True, check=True, stdout=subprocess.PIPE
        )
        distro = result.stdout.decode("utf-8").strip()

    if not distro:
        raise ValueError("Fail to detect distribution we are running on")

    return distro


if len(sys.argv) < 3:
    raise ValueError("Usage: service.py <action> <service>")

distro = get_linux_distribution()

args = {"act": quote_unix(sys.argv[1]), "service": quote_unix(sys.argv[2])}

print("Detected distro: %s" % (distro))

if re.search(distro, "Ubuntu"):
    if os.path.isfile("/etc/init/%s.conf" % args["service"]):
        cmd_args = ["service", args["service"], args["act"]]
    elif os.path.isfile("/etc/init.d/%s" % args["service"]):
        cmd_args = ["/etc/init.d/%s" % (args["service"]), args["act"]]
    else:
        print("Unknown service")
        sys.exit(2)
elif (
    re.search(distro, "Redhat")
    or re.search(distro, "Fedora")
    or re.search(distro, "CentOS Linux")
):
    cmd_args = ["systemctl", args["act"], args["service"]]

subprocess.call(cmd_args, shell=False)