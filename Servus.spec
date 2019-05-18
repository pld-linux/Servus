#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	C++ network utility library that provides a zeroconf API, URI parsing and UUIDs
Summary(pl.UTF-8):	Biblioteka narzędzi sieciowych udostępniająca API zeroconf, analizy URI i UUID
Name:		Servus
Version:	1.5.2
Release:	1
License:	LGPL v3
Group:		Libraries
#Source0Download: https://github.com/HBPVIS/Servus/releases
Source0:	https://github.com/HBPVIS/Servus/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bc6fb62a002fd288fc2c1f12878a533c
URL:		https://github.com/HBPVIS/Servus
BuildRequires:	Eyescale-CMake >= 2016.04
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	avahi-devel
# unit_test_framework
BuildRequires:	boost-devel >= 1.51
BuildRequires:	cmake >= 3.1
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Servus is a small C++ network utility library that provides a zeroconf
API, URI parsing and UUIDs.

%description -l pl.UTF-8
Servus to mała biblioteka C++ narzędzi sieciowych, udostępnikająca API
zeroconf, analizy URI i UUID.

%package devel
Summary:	Header files for Servus library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Servus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for Servus library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Servus.

%package qt
Summary:	Servus Qt library
Summary(pl.UTF-8):	Biblioteka Servus Qt
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description qt
Servus Qt library.

%description qt -l pl.UTF-8
Biblioteka Servus Qt.

%package qt-devel
Summary:	Header files for Servus Qt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Servus Qt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-qt = %{version}-%{release}
Requires:	Qt5Core-devel >= 5

%description qt-devel
Header files for Servus Qt library.

%description qt-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Servus Qt.

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

%package browser
Summary:	servusBrowser GUI
Summary(pl.UTF-8):	Graficzny interfejs servusBrowser
Group:		X11/Applications
Requires:	%{name}-qt = %{version}-%{release}

%description browser
servusBrowser GUI.

%description browser -l pl.UTF-8
Graficzny interfejs servusBrowser.

%prep
%setup -q

rmdir CMake/common
ln -s %{_datadir}/Eyescale-CMake CMake/common

%build
install -d build
cd build
%cmake .. \
	-DBUILDYARD_DISABLED=ON \
	-DCOMMON_DISABLE_WERROR:BOOL=ON
%{__make}

%if %{with apidocs}
doxygen doc/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_datadir}/Servus/CMake/ServusTargets.cmake

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	qt -p /sbin/ldconfig
%postun	qt -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS.txt AUTHORS.txt LICENSE.txt README.md doc/Changelog.md
%attr(755,root,root) %{_libdir}/libServus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libServus.so.6

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libServus.so
%dir %{_includedir}/servus
%{_includedir}/servus/*.h
%dir %{_datadir}/Servus
%{_datadir}/Servus/CMake

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libServusQt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libServusQt.so.6

%files qt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libServusQt.so
%{_includedir}/servus/qt

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif

%files browser
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/servusBrowser
