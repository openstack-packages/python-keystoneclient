#
# This is 2012.1 essex-3 milestone
#
%global release_name essex
%global release_letter e
%global milestone 3

Name:       python-keystoneclient
Version:    2012.1
Release:    0.1.%{release_letter}%{milestone}%{?dist}
Summary:    Python API and CLI for OpenStack Keystone

Group:      Development/Languages
License:    ASL 2.0
URL:        https://github.com/openstack/python-keystoneclient
BuildArch:  noarch

Source0:    http://launchpad.net/keystone/%{release_name}/%{release_name}-%{milestone}/+download/%{name}-%{version}~%{release_letter}%{milestone}.tar.gz

Requires:   python-simplejson
Requires:   python-httplib2
Requires:   python-prettytable

BuildRequires: python2-devel
BuildRequires: python-setuptools

%description
Client library and command line utility for interacting with Openstack
Keystone's API.

%package doc
Summary:    Documentation for OpenStack Keystone API Client
Group:      Documentation

Requires:   %{name} = %{version}-%{release}

BuildRequires: python-sphinx

%description doc
Documentation for the client library for interacting with Openstack
Keystone's API.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html docs html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc README.rst
%{_bindir}/keystone
%{python_sitelib}/keystoneclient
%{python_sitelib}/*.egg-info

%files doc
%doc html

%changelog
* Thu Jan 26 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-0.1.e3
- Initial package
