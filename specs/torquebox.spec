# jruby version used by torquebox
%define jrubie jruby-1.6.3

Summary: Ruby on JBoss...it goes to 11.
Name: torquebox
Version: 1.1.1
Release: %(echo ${BUILD_NUMBER:-1})
License: LGPL
Group: Applications/System
URL: http://torquebox.org
Source0: http://repository-torquebox.forge.cloudbees.com/release/org/torquebox/torquebox-dist/%{version}/torquebox-dist-%{version}-bin.zip
Source1: %{name}/%{name}.init
Source2: %{name}/%{name}.sysconfig
Source3: %{name}/%{name}.sh
Source6: %{name}/%{name}.gems
Source7: %{name}/%{name}.repo
Patch0: %{name}/server.xml.patch
Patch1: %{name}/run.sh.patch

Distribution: Centos 5
Packager: https://github.com/AncientLeGrey
Vendor: JBoss Community
BuildArch: noarch
BuildRoot: %{_topdir}/tmp

Requires: java >= 1.6.0

# https://github.com/torquebox/torquebox/blob/1.1.1/parent/pom.xml#L244
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
# set some variables in external sources
%define SOURCES %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE7} %{PATCH1}
sed -i    's|\${name}|%{name}|g'    %{SOURCES}
sed -i  's|\${jrubie}|%{jrubie}|g'  %{SOURCES}
sed -i  's|\${target}|%{target}|g'  %{SOURCES}
sed -i 's|\${version}|%{version}|g' %{SOURCES}
%patch0 -p1
%patch1 -p1


%install
mkdir -p %{buildroot}/%{target}
cp -R . %{buildroot}/%{target}
install -D %{SOURCE1} %{buildroot}/%{_initrddir}/%{name}
install -D %{SOURCE2} %{buildroot}/etc/sysconfig/%{name}
install -D %{SOURCE3} %{buildroot}/etc/profile.d/%{name}.sh
install -D %{SOURCE6} %{buildroot}/%{target}/%{jrubie}@%{name}.gems
install -D %{SOURCE7} %{buildroot}/etc/yum.repos.d/%{name}.repo
mkdir -p %{buildroot}/etc/%{name}.d

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
  getent group %{name} >/dev/null || /usr/sbin/groupadd -r %{name} || :
  getent passwd %{name}>/dev/null || /usr/sbin/useradd -r %{name} -g %{name} -d %{target} || :
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
%{target}
%defattr(-,root,root)
/%{_initrddir}/%{name}
/etc/profile.d/%{name}.sh
%config /etc/sysconfig/%{name}
%config %dir /etc/%{name}.d
%config /etc/yum.repos.d/%{name}.repo

%changelog
* Thu Oct 13 2011 https://github.com/AncientLeGrey
- Flagged config files
- Sysconfig file cleand up
* Thu Oct 13 2011 https://github.com/darrell
- Create torquebox user as system user
* Wed Aug 31 2011 https://github.com/AncientLeGrey - 1.1.1-1
- Moved sources into torquebox subdirectory
* Wed Aug 10 2011 https://github.com/AncientLeGrey - 1.1.1-1
- Update to version 1.1.1
  https://issues.jboss.org/secure/ReleaseNote.jspa?projectId=12310812&version=12317226
- Bugfix service clean script
- Fixed directory permissions
* Thu Jul 14 2011 https://github.com/AncientLeGrey - 1.1-1
- Clean option added to service script
- Update to version 1.1
  https://issues.jboss.org/secure/ReleaseNote.jspa?projectId=12310812&version=12316704
- Removed installation of rack and bundler gems, they are included in the
  torquebox binary distribution (TORQUE-423, TORQUE-424)
* Thu Jul 07 2011 https://github.com/AncientLeGrey - 1.0.1-2
- Source all files in /etc/torquebox.d at startup
* Wed Jul 06 2011 https://github.com/AncientLeGrey - 1.0.1-2
- Change default URIEncoding to UTF-8 in jbossweb connectors (http, ajp)
- Rvm gemset importfile cleanup
* Tue Jun 14 2011 https://github.com/AncientLeGrey - 1.0.1-2
- add bundlers gem bin path to PATH
- display JRUBY_HOME on login
* Fri Jun 10 2011 https://github.com/AncientLeGrey - 1.0.1-1
- Initial revision
