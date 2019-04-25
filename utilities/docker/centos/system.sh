echo '
#####################################
# DOCKER BUILD
#   system
#####################################
'

# Install needed system tools
yum update -y ; yum clean all
yum install systemd -y ; yum clean all
yum groupinstall "Development Tools" -y
yum install cmake -y 
yum install ncurses-devel -y
yum install epel-release -y
yum install libcurl-devel -y
yum install which -y

# python3 support needed as of 4.2
#yum --disablerepo="*" --enablerepo="epel" install python36 -y
#yum install python36 python36-devel python36-pip python36-tkinter -y
yum -y install wget
yum -y install gcc openssl-devel bzip2-devel
cd /usr/src
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
tar xzf Python-3.7.2.tgz
cd Python-3.7.2
./configure ––enable–optimizations
make altinstall
cd ../../..
[ -f /usr/bin/python3 ] || ln -s /usr/bin/python3.7 /usr/bin/python3
pip3 install matplotlib