Summary: X.Org X11 libXft runtime library
Name: libXft
Version: 2.1.7
Release: 5
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.x.org
Source0: http://xorg.freedesktop.org/X11R7.0-RC0/everything/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXrender-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel >= 2.2

Requires: fontconfig >= 2.2

Conflicts: XFree86-libs, xorg-x11-libs

%description
X.Org X11 libXft runtime library

%package devel
Summary: X.Org X11 libXft development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

Conflicts: XFree86-devel, xorg-x11-devel

%description devel
X.Org X11 libXft development package

%prep
%setup -q

# Disable static library creation by default.
%define with_static 0

%build

%configure \
%if ! %{with_static}
	--disable-static
%endif
make

%install

rm -rf $RPM_BUILD_ROOT
%makeinstall

# FIXME: There's no real good reason to ship these anymore, as pkg-config
# is the official way to detect flags, etc. now.
rm -f $RPM_BUILD_ROOT%{_bindir}/xft-config
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/xft-config*

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README INSTALL ChangeLog
%dir %{_libdir}
%{_libdir}/libXft.so.2
%{_libdir}/libXft.so.2.1.2

%files devel
%defattr(-,root,root,-)
%defattr(-,root,root,-)
#%{_bindir}/xft-config
%dir %{_includedir}/X11
%dir %{_includedir}/X11/Xft
%{_includedir}/X11/Xft/Xft.h
%{_includedir}/X11/Xft/XftCompat.h
%if %{with_static}
%{_libdir}/libXft.a
%endif
%{_libdir}/libXft.so
%{_libdir}/pkgconfig/xft.pc
%dir %{_mandir}
#%{_mandir}/man1/xft-config.1.gz
%dir %{_mandir}/man3
%{_mandir}/man3/Xft.3*

%changelog
* Thu Sep 29 2005 Mike A. Harris <mharris.com> 2.1.7-5
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro
- Fix BuildRequires to use new style X library package names

* Sun Sep 4 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-4
- Added "BuildRequires: fontconfig-devel >= 2.2" dependency that was
  previously missed.  Also added "Requires: fontconfig >= 2.2" runtime
  dependency.
- Added missing defattr to devel subpackage.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-3
- Added freetype-devel build dependency.

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-1
- Initial build.
