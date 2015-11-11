Name:       python-keystoneclient
# Since folsom-2 OpenStack clients follow their own release plan
# and restarted version numbering from 0.1.1
# https://lists.launchpad.net/openstack/msg14248.html
Epoch:      1
Version:    1.3.0
Release:    1%{?dist}
Summary:    Client library for OpenStack Identity API
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{name}
Source0:    http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr

# from requirements.txt
Requires: python-argparse
Requires: python-babel
Requires: python-iso8601 >= 0.1.4
Requires: python-netaddr
Requires: python-oslo-config >= 2:1.9.0
Requires: python-oslo-i18n >= 1.3.0
Requires: python-oslo-serialization >= 1.2.0
Requires: python-oslo-utils >= 1.2.0
Requires: python-prettytable
Requires: python-requests >= 2.2.0
Requires: python-six >= 1.9.0
Requires: python-stevedore >= 1.1.0
Requires: python-keystoneauth1 >= 1.0.0
Requires: python-pbr

# other requirements
Requires: python-setuptools
Requires: python-keyring
# for s3_token middleware
Requires: python-webob


%description
Client library and command line utility for interacting with Openstack
Identity API.

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
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -p -D -m 644 tools/keystone.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/keystone.bash_completion

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

# Build HTML docs and man page
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man
install -p -D -m 644 man/keystone.1 %{buildroot}%{_mandir}/man1/keystone.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/keystone
%{_sysconfdir}/bash_completion.d/keystone.bash_completion
%{python_sitelib}/keystoneclient
%{python_sitelib}/*.egg-info
%{_mandir}/man1/keystone.1*

%files doc
%doc LICENSE html

%changelog
