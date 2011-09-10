# TorqueBox RPM
TorqueBox RPM is a packaged version of the torquebox distribution provided by
[The TorqueBox Project](https://github.com/torquebox)


## Features
- Install TorqueBox with one single yum command
- Update to new versions with yum 
- Switch between bundled jruby and [rvm](https://rvm.beginrescueend.com/)
- Autoconfigure jruby environment for selected users


## Installation
Login as root and just type

```bash
yum -c http://bit.ly/torquebox-repo install torquebox
```

After that TorqueBox will be running as a service listening on port 8080.

### Install Documentation
Install a local copy of the torquebox docs with

```bash
yum install torquebox-docs
```

These docs are accessible at at http://localhost:8080/docs .


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
a gemset named jruby-1.6.3@torquebox.

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

### Cleanup torquebox
Sometimes its a good idea to delete the tmp, work, log and data/tx-object-store
directories to get rid of inconsistent temp data.

```bash
sudo service torquebox clean
```

does exactly that.

### Configuration
Any script in /etc/torquebox.d gets sourced. Put application level configuration
like JENKINS_HOME in there.


## Build

You can build the rpm by yourself.

### Locally
Use [cantiere](https://github.com/AncientLeGrey/cantiere) to download souces and
perform the rpmbuild.

```bash
rake rpm:torquebox
```

### Inside Overbox
An easier way to build the rpms is by using [overbox](https://github.com/AncientLeGrey/overbox):
Clone this repository into overbox projects directory and perform "vagrant reload".
After reload the jenkins job "torquebox.rpm-rpmbuild" sould appear. Execute this
job to build the rpms.


## Bugs
 - Please report rpm packaging related bugs to the [GitHub issue tracker](https://github.com/AncientLeGrey/torquebox.rpm/issues)
 - Bugs related to torquebox itself are reported to [TorqueBox Community: Issues](http://torquebox.org/community/issues/)
