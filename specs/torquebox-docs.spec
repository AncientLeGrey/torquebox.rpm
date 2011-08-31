Summary: TorqueBox html documentation
Name: torquebox-docs
Version: 1.1.1
Release: %(echo ${BUILD_NUMBER:-1})
License: LGPL
Group: Documentation
URL: http://torquebox.org/documentation
Source0: http://repository-torquebox.forge.cloudbees.com/release/org/torquebox/torquebox-docs-en_US/%{version}/torquebox-docs-en_US-%{version}-html.zip
Source1: %{name}/web.xml
Distribution: Centos 5
Packager: https://github.com/AncientLeGrey
Vendor: JBoss Community
BuildArch: noarch
BuildRoot: %{_topdir}/tmp

Requires: torquebox >= %{version}

%define target /var/lib/torquebox/apps/docs.war

%description
Installs torquebox html documentation into your local torquebox server at
context path /docs .

%prep
%setup -c %{name}

%install
mkdir -p %{buildroot}/%{target}/WEB-INF
cp -R . %{buildroot}/%{target}
install -D %{SOURCE1} %{buildroot}/%{target}/WEB-INF/web.xml

%clean
rm -Rf %{buildroot}

%files
%defattr(-,torquebox,torquebox)
/

%changelog
* Wed Aug 31 2011 https://github.com/AncientLeGrey - 1.1.1-1
- Initial revision
