%if 0%{?rhel} && 0%{?rhel} <= 6
%global __python2 %{_bindir}/python2
%global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_version %(%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])")
%endif

%if 0%{?fedora}
%global with_python3 1
%global _docdir_fmt %{name}
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-keystoneclient
# Since folsom-2 OpenStack clients follow their own release plan
# and restarted version numbering from 0.1.1
# https://lists.launchpad.net/openstack/msg14248.html
Epoch:      1
Version:    XXX
Release:    XXX
Summary:    Client library for OpenStack Identity API
License:    ASL 2.0
URL:        https://pypi.python.org/pypi/%{name}
Source0:    https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr >= 1.6
%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr >= 1.6
%endif

# from requirements.txt
%if 0%{?rhel} && 0%{?rhel} <= 6
Requires: python-argparse
%endif
Requires: python-babel
Requires: python-iso8601 >= 0.1.9
Requires: python-netaddr
Requires: python-oslo-config >= 2:3.7.0
Requires: python-oslo-i18n >= 2.1.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-utils >= 3.5.0
Requires: python-prettytable
Requires: python-requests >= 2.5.2
Requires: python-six >= 1.9.0
Requires: python-stevedore >= 1.5.0
Requires: python-pbr >= 1.6
Requires: python-debtcollector >= 1.2.0
Requires: python-positional >= 1.0.1
Requires: python-keystoneauth1 >= 2.1.0

# other requirements
Requires: python-setuptools
Requires: python-keyring
# for s3_token middleware
Requires: python-webob

Provides: python2-keystoneclient = %{epoch}:%{version}-%{release}


%description
Client library and command line utility for interacting with Openstack
Identity API.

%if 0%{?with_python3}
%package -n python3-keystoneclient
Summary:    Client library for OpenStack Identity API
# from requirements.txt
Requires: python3-babel
Requires: python3-iso8601 >= 0.1.9
Requires: python3-netaddr
Requires: python3-oslo-config >= 2:3.7.0
Requires: python3-oslo-i18n >= 2.1.0
Requires: python3-oslo-serialization >= 1.10.0
Requires: python3-oslo-utils >= 3.5.0
Requires: python3-prettytable
Requires: python3-requests >= 2.5.2
Requires: python3-six >= 1.9.0
Requires: python3-stevedore >= 1.5.0
Requires: python3-pbr >= 1.6
Requires: python3-debtcollector >= 1.2.0
Requires: python3-positional >= 1.0.1
Requires: python3-keystoneauth1 >= 2.1.0

# other requirements
Requires: python3-setuptools
Requires: python3-keyring
# for s3_token middleware
Requires: python3-webob

%description -n python3-keystoneclient
Client library for interacting with Openstack Identity API.
%endif # with_python3

%package doc
Summary:    Documentation for OpenStack Identity API Client
Group:      Documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx >= 2.3.0

%description doc
Documentation for the client library for interacting with Openstack
Identity API.

%prep
%setup -q -n %{name}-%{upstream_version}

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/tests
%if 0%{?with_python3}
rm -fr %{buildroot}%{python3_sitelib}/tests
%endif

# Build HTML docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-keystoneclient
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%endif # with_python3

%files doc
%doc html
%license LICENSE

%changelog
