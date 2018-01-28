#
# spec file for package rotter
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

%global commit 9a13295e83e213a805881129f9593ea332cdee36
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           rotter
Version:        0.9
Release:        2.20151103git%{shortcommit}%{?dist}
Summary:        Rotter is a Recording of Transmission / Audio Logger for JACK

License:        GPLv2
URL:            https://www.aelius.com/njh/rotter/
Source0:        https://github.com/njh/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# Fix custom strftime-style format layout
# https://github.com/njh/rotter/issues/29
Patch0:         https://github.com/radiorabe/%{name}/commit/d3c851053c83857fa39c06e67733e31e2bfe4071.diff

BuildRequires:  asciidoc
BuildRequires:  jack-audio-connection-kit-devel

%if %{with lame}
BuildRequires:  lame-devel
%endif

BuildRequires:  libsndfile-devel

%if %{with twolame}
BuildRequires:  twolame-devel
%endif

BuildRequires:  xmlto

%description
Rotter is a Recording of Transmission / Audio Logger for JACK. It was designed
for use by radio stations, who are legally required to keep a recording of all
their output. Rotter runs continuously, writing to a new file every hour.

Rotter can output files in servaral different strutures, including all files in
a single directory or create a directory structure.The advantage of using a
folder hierarchy is that you can store related files in the hour's directory.


%prep
%autosetup -n %{name}-%{commit} -p 1


%build
autoreconf -vi
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%doc ChangeLog README.md
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Sun Jan 28 2018 Christian Affolter <c.affolter@purplehaze.ch> - 0.9-2.20151103git9a13295
- Applying strftime-style format layout patch

* Thu Jan 25 2018 Christian Affolter <c.affolter@purplehaze.ch> - 0.9-1.20151103git9a13295
- Initial release

