#
# Conditional build:
%bcond_with	glew	# package also plain GLEW library

Summary:	The OpenGL Extension Wrangler Library
Summary(pl.UTF-8):	Bibliteka OpenGL Extension Wrangler
Name:		glew1
Version:	1.13.0
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/glew/glew-%{version}.tgz
# Source0-md5:	7cbada3166d2aadfc4169c4283701066
URL:		http://glew.sourceforge.net/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		pkgincludedir	%{_includedir}/glew1

%description
The OpenGL Extension Wrangler Library (GLEW) is a cross-platform C/C++
extension loading library. GLEW provides efficient run-time mechanisms
for determining which OpenGL extensions are supported on the target
platform. OpenGL core and extension functionality is exposed in a
single header file.

%description -l pl.UTF-8
OpenGL Extension Wrangler Library (GLEW) jest międzyplatformową
biblioteką C/C++ ładującą rozszerzenia. GLEW zapewnia wydajne
mechanizmy rozpoznające które rozszerzenia są dostępne w czasie
wykonywania programu. Funkcjonalność rdzenia OpenGL i rozszerzeń jest
udostępniana w pojedynczym pliku nagłówkowym.

%package devel
Summary:	Development files for GLEW library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki GLEW
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-headers = %{version}-%{release}
Requires:	OpenGL-GLU-devel
Requires:	xorg-lib-libX11-devel

%description devel
Development files for GLEW library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki GLEW.

%package static
Summary:	Static GLEW library
Summary(pl.UTF-8):	Biblioteka statyczna GLEW
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GLEW library.

%description static -l pl.UTF-8
Biblioteka statyczna GLEW.

%package headers
Summary:	GLEW header files
Summary(pl.UTF-8):	Pliki nagłówkowe GLEW
Group:		Development/Libraries

%description headers
GLEW header files.

%description headers -l pl.UTF-8
Pliki nagłówkowe GLEW.

%package mx
Summary:	GLEW MX library
Summary(pl.UTF-8):	Biblioteka GLEW MX
Group:		Libraries

%description mx
GLEW MX library (GLEW for multiple rendering contexts).

%description mx -l pl.UTF-8
Biblioteka GLEW MX (GLEW dla wielu kontekstów renderujących).

%package mx-devel
Summary:	Development files for GLEW MX library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki GLEW MX
Group:		Development/Libraries
Requires:	%{name}-mx = %{version}-%{release}
Requires:	%{name}-headers = %{version}-%{release}
Requires:	OpenGL-GLU-devel
Requires:	xorg-lib-libX11-devel

%description mx-devel
Development files for GLEW MX library.

%description mx-devel -l pl.UTF-8
Pliki programistyczne biblioteki GLEW MX.

%package mx-static
Summary:	Static GLEW MX library
Summary(pl.UTF-8):	Biblioteka statyczna GLEW MX
Group:		Development/Libraries
Requires:	%{name}-mx-devel = %{version}-%{release}

%description mx-static
Static GLEW MX library.

%description mx-static -l pl.UTF-8
Biblioteka statyczna GLEW MX.

%prep
%setup -q -n glew-%{version}

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	INCDIR=%{pkgincludedir}/GL \
	LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install%{!?with_glew:.mx} \
	DESTDIR=$RPM_BUILD_ROOT \
	INCDIR=%{pkgincludedir}/GL \
	LIBDIR=%{_libdir}

# Win32-specific
%{__rm} $RPM_BUILD_ROOT%{pkgincludedir}/GL/wglew.h

%if %{with glew}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/{libGLEW.so,libGLEW1.so}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/{libGLEW.a,libGLEW1.a}
%{__mv} $RPM_BUILD_ROOT%{_pkgconfigdir}/{glew,glew1}.pc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	mx -p /sbin/ldconfig
%postun	mx -p /sbin/ldconfig

%if %{with glew}
%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.txt TODO.txt doc/*.{html,css,png,jpg}
%attr(755,root,root) %{_libdir}/libGLEW.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLEW.so.1.13

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLEW1.so
%{_pkgconfigdir}/glew1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libGLEW1.a
%endif

%files headers
%defattr(644,root,root,755)
%dir %{pkgincludedir}
%dir %{pkgincludedir}/GL
%{pkgincludedir}/GL/glew.h
%{pkgincludedir}/GL/glxew.h

%files mx
%defattr(644,root,root,755)
%doc LICENSE.txt README.txt TODO.txt doc/*.{html,css,png,jpg}
%attr(755,root,root) %{_libdir}/libGLEWmx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLEWmx.so.1.13

%files mx-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLEWmx.so
%{_pkgconfigdir}/glewmx.pc

%files mx-static
%defattr(644,root,root,755)
%{_libdir}/libGLEWmx.a
