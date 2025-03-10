#
# TODO:
# - when updating, check if we can get rid of -no-save-flag patch in targetcli
#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	rtslib_fb
Summary:	Python library for configuring the Linux kernel-based multiprotocol SCSI target (LIO)
Name:		python-rtslib-fb
Version:	2.1.70
Release:	6
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/open-iscsi/rtslib-fb/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	9ebdd1dc80537ffd5a92178621e8cc47
URL:		https://github.com/open-iscsi/rtslib-fb
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python3-modules
%endif
Requires:	python-modules
Requires:	python-pyudev >= 0.16.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rtslib-fb is an object-based Python library for configuring the LIO
generic SCSI target, present in 3.x Linux kernel versions.

%package -n python3-rtslib-fb
Summary:	Python library for configuring the Linux kernel-based multiprotocol SCSI target (LIO)
Group:		Libraries/Python
Requires:	python3-pyudev >= 0.16.1

%description -n python3-rtslib-fb
rtslib-fb is an object-based Python library for configuring the LIO
generic SCSI target, present in 3.x Linux kernel versions.

%prep
%setup -q -n rtslib-fb-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
%{__rm} -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man{5,8}

%if %{with python2}
%py_install

# symlink for old module name
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/rtslib
ln -sf %{py_sitescriptdir}/%{module} $RPM_BUILD_ROOT%{py_sitescriptdir}/rtslib

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/targetctl{,2}
cp doc/targetctl.8 $RPM_BUILD_ROOT%{_mandir}/man8/targetctl2.8
%endif

%if %{with python3}
%py3_install

# symlink for old module name
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/rtslib
ln -sf %{py3_sitescriptdir}/%{module} $RPM_BUILD_ROOT%{py3_sitescriptdir}/rtslib
cp doc/targetctl.8 $RPM_BUILD_ROOT%{_mandir}/man8/
%endif

cp -p doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5/

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/targetctl2
%dir %{py_sitescriptdir}/%{module}
%ghost %{py_sitescriptdir}/rtslib
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/rtslib_fb-*.egg-info
%{_mandir}/man8/targetctl2.8*
%endif

%if %{with python3}
%files -n python3-rtslib-fb
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/targetctl
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/rtslib
%{py3_sitescriptdir}/rtslib_fb-*-py*.egg-info
%{_mandir}/man5/saveconfig.json.5*
%{_mandir}/man8/targetctl.8*
%endif
