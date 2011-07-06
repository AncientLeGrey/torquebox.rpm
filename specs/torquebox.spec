# jruby version used by torquebox
%define jrubie jruby-1.6.2

Summary: Ruby on JBoss...it goes to 11.
Name: torquebox
Version: 1.0.1
Release: %(echo ${BUILD_NUMBER:-2})
License: LGPL
Group: Applications/System
URL: http://torquebox.org
Source0: http://repository-torquebox.forge.cloudbees.com/release/org/torquebox/torquebox-dist/%{version}/torquebox-dist-%{version}-bin.zip
Source1: %{name}.init
Source2: %{name}.sysconfig
Source3: %{name}.sh
Source4: http://rubygems.org/downloads/bundler-1.0.14.gem
Source5: http://rubygems.org/downloads/rack-1.3.0.gem
Source6: %{name}.gems
Source7: %{name}.repo
Patch0: server.xml.patch

Distribution: Centos 5
Packager: https://github.com/AncientLeGrey
Vendor: JBoss Community
BuildArch: noarch
BuildRoot: %{_topdir}/tmp

Requires: java >= 1.6.0

# https://github.com/torquebox/torquebox/blob/1.0.1/parent/pom.xml#L244
Provides: jruby = %{jrubie}
Provides: hornetq = 2.0.0.GA
Provides: jbossas = 6.0.0.Final

# http://www.redhat.com/archives/rhl-list/2008-June/msg01371.html
%define __jar_repack %{nil}
# installation target dir
%define target /var/lib/%{name}

%description
TorqueBox is a new kind of Ruby application platform that integrates popular
technologies such as Ruby on Rails, while extending the footprint of Ruby
applications to include built-in support for services such as messaging,
scheduling, and daemons.
TorqueBox provides an all-in-one environment, built upon the latest, most
powerful JBoss AS Java application server. Functionality such as clustering,
load-balancing and high-availability is included right out-of-the-box.


%prep
%setup -n %{name}-%{version}
%patch0 -p1
# set some variables in external sources
%define SOURCES %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE7}
sed -i    's|\${name}|%{name}|g'    %{SOURCES}
sed -i  's|\${jrubie}|%{jrubie}|g'  %{SOURCES}
sed -i  's|\${target}|%{target}|g'  %{SOURCES}
sed -i 's|\${version}|%{version}|g' %{SOURCES}

# https://issues.jboss.org/browse/TORQUE-424
./jruby/bin/jruby -S gem install %{SOURCE4} --install-dir ./jruby/lib/ruby/gems/1.8
# https://issues.jboss.org/browse/TORQUE-423
./jruby/bin/jruby -S gem install %{SOURCE5} --install-dir ./jruby/lib/ruby/gems/1.8


%install
mkdir -p %{buildroot}/%{target}
cp -R . %{buildroot}/%{target}
install -D %{SOURCE1} %{buildroot}/%{_initrddir}/%{name}
install -D %{SOURCE2} %{buildroot}/etc/sysconfig/%{name}
install -D %{SOURCE3} %{buildroot}/etc/profile.d/%{name}.sh
install -D %{SOURCE6} %{buildroot}/%{target}/%{jrubie}@%{name}.gems
install -D %{SOURCE7} %{buildroot}/etc/yum.repos.d/%{name}.repo

# http://www.redhat.com/archives/rpm-list/2003-February/msg00002.html
chmod -x %{buildroot}/%{target}/jboss/bin/jboss_init_solaris.sh

# torquebox members should be able to mange gems and do deployments
chmod 775 -R %{buildroot}/%{target}/jruby/lib/ruby/gems
chmod 775 -R %{buildroot}/%{target}/jruby/bin
chmod 775 %{buildroot}/%{target}/apps
chmod 644 %{buildroot}/etc/sysconfig/%{name}

# backstage deploy wants to change this file
chmod 775 %{buildroot}/%{target}/jboss/server/default/conf/props/torquebox-users.properties


%clean
rm -Rf %{buildroot}


# http://www.rpm.org/max-rpm/s1-rpm-inside-scripts.html#S2-RPM-INSIDE-ERASE-TIME-SCRIPTS
%pre
if [ "$1" = 1 ]
then
  getent group %{name} >/dev/null || /usr/sbin/groupadd %{name} || :
  /usr/sbin/useradd %{name} -g %{name} || :
else
  /sbin/service %{name} stop || :
fi


%post
if [ "$1" = 1 ]
then
  /sbin/chkconfig --add %{name}
  /sbin/chkconfig %{name} on
fi
/sbin/service %{name} start


%preun
if [ "$1" = 0 ]
then
  /sbin/chkconfig --del %{name} || :
  /sbin/service %{name} stop || :
fi


%postun
if [ "$1" = 0 ]
then
  /usr/sbin/userdel -r %{name} || :
fi


%files
%defattr(-,%{name},%{name})
/


%changelog
* Wed Jul 06 2011 https://github.com/AncientLeGrey - 1.0.1-2
- Change default URIEncoding to UTF-8 in jbossweb connectors (http, ajp)
* Tue Jun 14 2011 https://github.com/AncientLeGrey - 1.0.1-2
- add bundlers gem bin path to PATH
- display JRUBY_HOME on login
* Fri Jun 10 2011 https://github.com/AncientLeGrey - 1.0.1-1
- Initial revision
