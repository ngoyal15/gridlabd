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
yum -y update
yum -y install wget
yum -y install gcc openssl-devel bzip2-devel
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
tar xzf Python-3.7.2.tgz
cd Python-3.7.2
./configure --enable-optimizations
yum -y install libffi-devel
make altinstall
cd -