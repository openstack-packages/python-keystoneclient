Name:       python-keystoneclient
# Since folsom-2 OpenStack clients follow their own release plan
# and restarted version numbering from 0.1.1
# https://lists.launchpad.net/openstack/msg14248.html
Epoch:      1
Version:    0.2.5
Release:    2%{?dist}
Summary:    Client library for OpenStack Identity API
License:    ASL 2.0
URL:        http://pypi.python.org/pypi/%{name}
Source0:    http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

#
# patches_base=0.2.5
#
Patch0001: 0001-Remove-runtime-dependency-on-python-pbr.patch
Patch0002: 0002-Add-find-method-to-CrudManager.patch
Patch0003: 0003-Allow-keystoneclient-to-work-with-older-keystone-ins.patch
Patch0004: 0004-Fix-optional-keyring-support-add-basic-keyring-tests.patch
Patch0005: 0005-Cleanup-shell-s-authentication-check.patch
Patch0006: 0006-Provide-keystone-CLI-man-page.patch
Patch0007: 0007-Use-AuthRef-for-some-client-fields.patch
Patch0008: 0008-Fix-memcache-encryption-middleware.patch
Patch0009: 0009-Change-memcache-config-entry-name-in-Keystone-to-be-.patch
Patch0010: 0010-Implements-v3-auth-client.patch
Patch0011: 0011-Python-2.6-compatibility-for-tests-test_keyring.py.patch

BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-d2to1

# from requirements.txt
Requires: python-argparse
Requires: python-iso8601 >= 0.1.4
Requires: python-prettytable
Requires: python-requests >= 0.8.8
Requires: python-simplejson
Requires: python-oslo-config >= 1.1.0
Requires: python-d2to1
Requires: python-six
# other requirements
Requires: python-setuptools
Requires: python-keyring
Requires: python-webob


%description
Client library and command line utility for interacting with Openstack
Identity API.

%package doc
Summary:    Documentation for OpenStack Identity API Client
Group:      Documentation

BuildRequires: python-sphinx

%description doc
Documentation for the client library for interacting with Openstack
Identity API.

%prep
%setup -q

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1

# We provide version like this in order to remove runtime dep on pbr.
sed -i s/REDHATKEYSTONECLIENTVERSION/%{version}/ keystoneclient/__init__.py

# Remove bundled egg-info
rm -rf python_keystoneclient.egg-info
# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -p -D -m 644 tools/keystone.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/keystone.bash_completion

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/keystone
%{_sysconfdir}/bash_completion.d/keystone.bash_completion
%{python_sitelib}/keystoneclient
%{python_sitelib}/*.egg-info

%files doc
%doc LICENSE doc/build/html

%changelog
* Tue Jun 25 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.5-2
- Remove runtime dependency on python-pbr.

* Tue Jun 25 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.5-1
- Update to latest upstream. (0.2.5 + patches)
- Add new python requires from requirements.txt. (d2to1, pbr, six)

* Tue May 28 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-4
- Check token expiry. (CVE-2013-2104)

* Thu May 02 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-3
- Config value for revocation list timeout. (#923519)

* Thu Apr 04 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-2
- Update requires. (#948244)

* Tue Mar 19 2013 Alan Pevec <apevec@redhat.com> 0.2.3-1
- New upstream release.

* Wed Jan 30 2013 Alan Pevec <apevec@redhat.com> 0.2.2-1
- New upstream release.

* Thu Jan 17 2013 Alan Pevec <apevec@redhat.com> 0.2.1-2
- Add dependency on python-requests.
- Add python-keyring RPM dependency.

* Fri Dec 21 2012 Alan Pevec <apevec@redhat.com> 0.2.1-1
- New upstream release.
- Add bash completion support

* Fri Nov 23 2012 Alan Pevec <apevec@redhat.com> 0.2.0-1
- New upstream release.
- Identity API v3 support
- add service_id column to endpoint-list
- avoid ValueError exception for 400 or 404 lp#1067512
- use system default CA certificates lp#106483
- keep original IP lp#1046837
- avoid exception for an expected empty catalog lp#1070493
- fix keystoneclient against Rackspace Cloud Files lp#1074784
- blueprint solidify-python-api
- blueprint authtoken-to-keystoneclient-repo
- fix auth_ref initialization lp#1078589
- warn about bypassing auth on CLI lp#1076225
- check creds before token/endpoint lp#1076233
- check for auth URL before password lp#1076235
- fix scoped auth for non-admins lp#1081192

* Tue Oct 16 2012 Alan Pevec <apevec@redhat.com> 0.1.3.27-1
- Allow empty description for tenants (lp#1025929)
- Documentation updates
- change default  wrap for tokens from 78 characters to 0 (lp#1061514)
- bootstrap a keystone user in one cmd
- Useful message when missing catalog (lp#949904)

* Thu Sep 27 2012 Alan Pevec <apevec@redhat.com> 1:0.1.3.9-1
- Handle "503 Service Unavailable" exception (lp#1028799)
- add --wrap option for long PKI tokens (lp#1053728)
- remove deprecated Diablo options
- add --os-token and --os-endpoint options to match
  http://wiki.openstack.org/UnifiedCLI/Authentication

* Sun Sep 23 2012 Alan Pevec <apevec@redhat.com> 1:0.1.3-1
- Change underscores in new cert options to dashes (lp#1040162)

* Wed Aug 22 2012 Alan Pevec <apevec@redhat.com> 1:0.1.2-1
- Add dependency on python-setuptools (#850842)
- New upstream release.

* Mon Jul 23 2012 Alan Pevec <apevec@redhat.com> 1:0.1.1-1
- New upstream release.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2-0.2.f1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 05 2012 Alan Pevec <apevec@redhat.com> 2012.1-1
- Essex release

* Thu Apr 05 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.8.rc2
- essex rc2

* Sat Mar 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.7.rc1
- update to final essex rc1

* Wed Mar 21 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.6.rc1
- essex rc1

* Thu Mar 01 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.5.e4
- essex-4 milestone

* Tue Feb 28 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.4.e4
- Endpoints: Add create, delete, list support
  https://review.openstack.org/4594

* Fri Feb 24 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.3.e4
- Improve usability of CLI. https://review.openstack.org/4375

* Mon Feb 20 2012 Alan Pevec <apevec@redhat.com> 2012.1-0.2.e4
- pre essex-4 snapshot, for keystone rebase

* Thu Jan 26 2012 Cole Robinson <crobinso@redhat.com> - 2012.1-0.1.e3
- Initial package
