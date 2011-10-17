Summary: SELinux policy for torquebox
Name: torquebox-selinux-policy
Version: 1.1.1
Release: %(echo ${BUILD_NUMBER:-2})
License: LGPL
Group: Applications/System
URL: http://torquebox.org
Source200: %{name}/torquebox.te
Source201: %{name}/torquebox.fc.in
Source202: %{name}/torquebox.if

Distribution: Centos 5
Packager: https://github.com/AncientLeGrey
Vendor: JBoss Community
BuildArch: %{_arch}
BuildRoot: %{_topdir}/tmp

Requires: torquebox >= %{version}

BuildRequires: libselinux-devel
%if (0%{?rhel_version} > 0 && 0%{?rhel_version} < 600) || (0%{?centos_version} > 0 && 0%{?centos_version} < 600)
BuildRequires: selinux-policy
%else
BuildRequires: selinux-policy-devel
%endif

%define target /var/lib/torquebox

%description
SELinux policy for torquebox


%prep
%setup -c -T
cp %{SOURCE200} %{SOURCE202} .
sed -e 's,@_VAR@,%{_var},' -e 's,@TARGET@,%{target},' -e 's,@_INITDDDIR@,%{_initddir},' %{SOURCE201} > torquebox.fc


%build
make -f %{_datadir}/selinux/devel/Makefile


%install
install -p -m 644 -D torquebox.pp %{buildroot}%{_datadir}/selinux/packages/torquebox/torquebox.pp

%clean
rm -Rf %{buildroot}


%post
semodule -i %{sharedir}/selinux/packages/torquebox/torquebox.pp 2>/dev/null || :
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 1090-1091
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 1098-1099
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 3873
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 4446
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 4712
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 4714
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 5445
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 5455
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 5500-5501
/usr/sbin/semanage port -a -t torquebox_port_t -p tcp 8083


%preun
if [ "$1" = 0 ]
then
  semodule -r %{name} 2>/dev/null || :
fi


%postun
if [ "$1" -ge "1" ] ; then # Upgrade
  semodule -i %{_datadir}/selinux/packages/%{name}/%{name}.pp 2>/dev/null || :
fi


%files
%{_datadir}/selinux/packages/torquebox/torquebox.pp


%changelog
* Thu Oct 13 2011 Darrell Fuhriman - 1.1.1-2
- Added selinux support. 
