#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	C++ network utility library that provides a zeroconf API, URI parsing and UUIDs.
Name:		Servus
Version:	1.3.0
Release:	1
License:	LGPL v3
Group:		Libraries
Source0:	https://github.com/HBPVIS/Servus/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	948efe958d3c9586a06d0c1e10d1d74e
URL:		https://github.com/HBPVIS/Servus
BuildRequires:	Eyescale-CMake >= 2016.04
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	avahi-devel
BuildRequires:	boost-devel >= 1.41.0
BuildRequires:	cmake >= 2.8
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Servus is a small C++ network utility library that provides a zeroconf
API, URI parsing and UUIDs.

%package devel
Summary:	Header files for Servus library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Servus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Servus library.

%package apidocs
Summary:	Servus API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Servus
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Servus library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Servus.

%prep
%setup -q

ln -s %{_datadir}/Eyescale-CMake CMake/common
%{__rm} .gitexternals

%build
install -d build
cd build
%cmake .. \
	-DBUILDYARD_DISABLED=ON
%{__make}

%if %{with apidocs}
doxygen doc/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.md doc/Changelog.md
%attr(755,root,root) %{_bindir}/servusBrowser
%attr(755,root,root) %{_libdir}/libServus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libServus.so.3
%attr(755,root,root) %{_libdir}/libServusQt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libServusQt.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libServus.so
%attr(755,root,root) %ghost %{_libdir}/libServusQt.so
%{_includedir}/servus
%dir %{_datadir}/Servus
%{_datadir}/Servus/CMake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
