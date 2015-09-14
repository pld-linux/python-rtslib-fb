#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	rtslib
Summary:	Python library for configuring the Linux kernel-based multiprotocol SCSI target (LIO)
Name:		python-rtslib-fb
Version:	2.1.fb50
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://codeload.github.com/agrover/rtslib-fb/tar.gz/v%{version}
# Source0-md5:	2eccddc0c6061590250f2d358fafdad7
URL:		https://github.com/agrover/rtslib-fb
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rtslib-fb is an object-based Python library for configuring the LIO
generic SCSI target, present in 3.x Linux kernel versions.

%package -n python3-rtslib-fb
Summary:	Python library for configuring the Linux kernel-based multiprotocol SCSI target (LIO)
Group:		Libraries/Python

%description -n python3-rtslib-fb
rtslib-fb is an object-based Python library for configuring the LIO
generic SCSI target, present in 3.x Linux kernel versions.

%prep
%setup -q -n rtslib-fb-%{version}

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man{5,8}

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
%endif

cp doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5/
cp doc/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/targetctl
%doc README.md
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/rtslib_fb-*.egg-info
%endif
%endif
%{_mandir}/man5/saveconfig.json.5*
%{_mandir}/man8/targetctl.8*

%if %{with python3}
%files -n python3-rtslib-fb
%defattr(644,root,root,755)
%doc README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/rtslib_fb-*-py*.egg-info
%endif
