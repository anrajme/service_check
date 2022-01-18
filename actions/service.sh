#service $2 $1
function get_linux_distribution() {
  distro=`lsb_release -s -i`
}


function main() {
act=$1
service=$2
echo $act
echo $service
if [ $# -lt 2 ]
  then
    echo "Usage: service.py <action> <service>"
    exit 0
fi
get_linux_distribution
osystem=$distro


if [ "$osystem" ] == "Ubuntu"
  then
    /etc/init.d/$service $act
elif [ $osystem == "Redhat" ] || [ $osystem == "Fedora" ] || [ $osystem == "CentOS" ]
  then
  systemctl $service $act
else
   echo "Unsupported Operating System"
fi

}

main
