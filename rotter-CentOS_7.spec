#
# spec file for package rotter (dedicated for OBS)
#
# Copyright (c) 2018 Radio Bern RaBe
#                    http://www.rabe.ch
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public 
# License as published  by the Free Software Foundation, version
# 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License  along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Please submit enhancements, bugfixes or comments via GitHub:
# https://github.com/radiorabe/centos-rpm-rotter
#

# Conditional build support
# add --without lame option, i.e. enable lame by default
%bcond_without lame
# add --without twolame option, i.e. enable twolame by default
%bcond_without twolame

%global commit a5538b76da5f0933361509eb2322afbffedf890c
%global shortcommit a5538b7

Name:           rotter
Version:        0.9

# OpenSUSE Build Service (OBS) replaces the whole Release string with only
# <CI_CNT>.<B_CNT> by default, this drops the post release git info string.  As
# a workaround, the <CI_CNT>.<B_CNT> will be explicitly set, in order to retain
# the Git snapshot information.
# https://en.opensuse.org/openSUSE:Build_Service_Tips_and_Tricks#How_to_control_a_Release_number_of_resulted_packages
Release:        <CI_CNT>.<B_CNT>.20180129git%{shortcommit}%{?dist}
Summary:        Rotter is a Recording of Transmission / Audio Logger for JACK

License:        GPLv2
URL:            https://www.aelius.com/njh/rotter/
Source0:        https://github.com/njh/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{name}@.service
Source2:        jackd@.service
Source3:        dbus-%{name}.conf

BuildRequires:  asciidoc
BuildRequires:  jack-audio-connection-kit-devel

%if %{with lame}
BuildRequires:  lame-devel
%endif

BuildRequires:  libsndfile-devel

%if %{with twolame}
BuildRequires:  twolame-devel
%endif

%{?systemd_requires}
BuildRequires: systemd

BuildRequires:  xmlto

Requires(pre): shadow-utils
# Required for the jackd@.service systemd service unit template
Requires: jack-audio-connection-kit-example-clients


%description
Rotter is a Recording of Transmission / Audio Logger for JACK. It was designed
for use by radio stations, who are legally required to keep a recording of all
their output. Rotter runs continuously, writing to a new file every hour.

Rotter can output files in servaral different strutures, including all files in
a single directory or create a directory structure.The advantage of using a
folder hierarchy is that you can store related files in the hour's directory.


%prep
%autosetup -n %{name}-%{commit}


%build
autoreconf -vi
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

# Install the systemd service unit
install -d %{buildroot}/%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}

# Install the dbus rotter configuration
install -d %{buildroot}/%{_sysconfdir}/dbus-1/system.d
install -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/dbus-1/system.d/%{name}.conf

# rotter recording instance root and home directory
install -d %{buildroot}/%{_sharedstatedir}/%{name}


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d /var/lib/%{name} -s /sbin/nologin \
    -c "%{name} system user account" %{name}
exit 0


%files
%doc ChangeLog README.md
%{_bindir}/*
%{_mandir}/man1/*
%{_unitdir}/*

# Install dbus system configuration to run jackd in headless mode
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/%{name}.conf

# rotter recording instance root and home directory
%dir %attr(0755, %{name}, %{name}) %{_sharedstatedir}/%{name}


%changelog
* Tue Feb 06 2018 Christian Affolter <c.affolter@purplehaze.ch> - 0.9-4.20180129gita5538b7
- Add systemd service units
- Create rotter system user/group
- Add D-Bus configuration to run jackd in headless mode

* Mon Jan 29 2018 Christian Affolter <c.affolter@purplehaze.ch> - 0.9-3.20180130gita5538b7
- Bump to a5538b7 (2018-01-29) which includes the previous strftime-style-layout
  patch

* Sun Jan 28 2018 Christian Affolter <c.affolter@purplehaze.ch> - 0.9-2.20151103git9a13295
- Applying strftime-style format layout patch

* Thu Jan 25 2018 Christian Affolter <c.affolter@purplehaze.ch> - 0.9-1.20151103git9a13295
- Initial release

