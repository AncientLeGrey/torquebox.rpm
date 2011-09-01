%define torquebox_home /var/lib/torquebox
%define target         %{torquebox_home}/apps
%define jruby_home     %{torquebox_home}/jruby
%define jruby_bin_path %{jruby_home}/bin
%define gem_path       %{jruby_home}/lib/ruby/gems/1.8

%define gem_install() (jruby -S gem install %* --ignore-dependencies -i %{buildroot}/%{gem_path} -n %{buildroot}/%{jruby_bin_path})

Summary: Look behind the TorqueBox curtain
Name: torquebox-backstage
Version: 0.5.2
Release: %(echo ${BUILD_NUMBER:-1})
License: LGPL
Group: Development/Tools
URL: http://torquebox.org/backstage/

Source0: %{name}/%{name}-knob.yml
Source1: http://rubygems.org/downloads/torquebox-backstage-0.5.2.gem
Source2: http://rubygems.org/downloads/haml-3.1.1.gem
Source3: http://rubygems.org/downloads/json-1.5.1-java.gem
Source4: http://rubygems.org/downloads/rack-accept-0.4.4.gem
Source5: http://rubygems.org/downloads/rack-flash-0.1.1.gem
Source6: http://rubygems.org/downloads/sass-3.1.2.gem
Source7: http://rubygems.org/downloads/sinatra-1.2.6.gem
Source8: http://rubygems.org/downloads/tilt-1.3.2.gem
Source9: http://rubygems.org/downloads/tobias-jmx-0.8.gem
Source10: http://rubygems.org/downloads/tobias-sinatra-url-for-0.2.1.gem

Distribution: Centos 5
Packager: https://github.com/AncientLeGrey
Vendor: JBoss Community
BuildArch: noarch
BuildRoot: %{_topdir}/tmp

Requires: torquebox = 1.1.1

%description
BackStage allows you to look behind the TorqueBox curtain, and view information
about all of the components you have running. It includes support for remote
code execution and log tailing to aid in debugging.

This RPM deployes backstage at context /backstage without authentication.
To enable authentication redeploy backstage with the following command:

  jruby -S backstage deploy --secure=username:password

%prep
%setup -T -c %{name}

%install
mkdir -p %{buildroot}/%{target}
install -D %{SOURCE0} %{buildroot}/%{target}/%{name}-knob.yml
%gem_install %{_sourcedir}/*.gem

%clean
rm -Rf %{buildroot}

%files
%defattr(775,torquebox,torquebox)
/

%changelog
* Thu Sep 01 2011 https://github.com/AncientLeGrey - 0.5.2-1
- Initial revision
