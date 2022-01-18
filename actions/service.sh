function get_linux_distribution() {
  distro=`lsb_release -s -i`
}

act=$1
service=$2

if [ $# -lt 2 ]
  then
    echo "Usage: service.py <action> <service>"
    exit 0
fi

get_linux_distribution

if [ $distro == 'Ubuntu' ]
  then
    /etc/init.d/$service $act
elif [[ $distro == "Redhat" ||  $distro == "Fedora"  ||  $distro == "CentOS" ]]
  then
    systemctl $service $act
else
   echo "Unsupported Operating System"
fi