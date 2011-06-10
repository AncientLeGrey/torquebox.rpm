# TorquBox RPM
TorquBox RPM is a packaged version of the torquebox distribution provided by
[The TorqueBox Project](https://github.com/torquebox)


## Features
- Install TorquBox with one single yum command
- Update to new versions with yum 
- Switch between bundled jruby and [rvm](https://rvm.beginrescueend.com/)
- Autoconfigure jruby environment for selected users


## Build
You can build the rpm by yourself. Use
[cantiere](https://github.com/AncientLeGrey/cantiere) to download souces and
perform the rpmbuild.

```bash
rake rpm:torquebox
```

There is also a jenkins job in .jenkins/rpmbuild .
This job requires [cantiere.rpm](https://github.com/AncientLeGrey/overbox-base-rpms)
to be installed


## Installation
Login as root and just type

```bash
yum -y -c http://dl.dropbox.com/u/153388/torquebox.rpm/torquebox.repo install torquebox
or
rpm -Uvh http://dl.dropbox.com/u/153388/torquebox.rpm/noarch/torquebox-1.0.1-1.noarch.rpm
```

After that TorqueBox will be running as a service listening on port 8080.

## Usage

### Deploying
To do deployments join the group torquebox and relogin. This will setup the
right ruby environment for the user.

```bash
gpasswd -a <username> torquebox
su - <username>
rake torquebox:deploy
```

### Managing gems
Join torquebox as your primary group to install or update gems

```bash
newgrp torquebox
gem install ...
exit
```

### Switching to rvm
Switching to rvm means that the torquebox server joins the group rvm und uses
a gemset named jruby-1.6.2@torquebox.

When you switch to rvm the first time, jruby and the torquebox-gems will be 
installed. Use the --no-install option to avoid this.

After switching, relogin with you development user to gain the new jruby environment.

```bash
sudo service torquebox use rvm
```

### Switching back to bundle jruby

```bash
sudo service torquebox use bundled
```

### Managing torquebox

```bash
sudo service torquebox (start|stop|restart)
```


## Bugs
Please report bugs with the GitHub issue tracker.
