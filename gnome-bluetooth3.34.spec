%define major		13
%define gi_major	1.0

%define libname		%mklibname %{name} %{major}
%define develname	%mklibname -d %{name}
%define girname		%mklibname %{name}-gir %{gi_major}

%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1
%define oname gnome-bluetooth

Name: 	 	gnome-bluetooth3.34
Summary: 	GNOME Bluetooth Subsystem
Version:	3.34.5
Release:	6
Source0:	http://download.gnome.org/sources/gnome-bluetooth/%{url_ver}/gnome-bluetooth-%{version}.tar.xz
Source1:	61-gnome-bluetooth-rfkill.rules
Patch0:		755fd758f866d3a3f7ca482942beee749f13a91e.patch
URL:		http://usefulinc.com/software/gnome-bluetooth/
#gw lib is LGPL, main app is GPL
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.29.90
BuildRequires:	pkgconfig(gmodule-2.0)
BuildRequires:	pkgconfig(gmodule-export-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libnotify) >= 0.7.0
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	python3dist(python-dbusmock)
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.9.5
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	libxml2-utils
BuildRequires:  meson
BuildRequires:  gtk-doc
Requires:	gvfs-obexftp
Requires:	bluez
Requires:	obexd
Requires:	pulseaudio-module-bluetooth
#Provides:	bluez-pin

%description
The gnome-bluetooth package contains graphical utilities to setup,
monitor and use Bluetooth devices.

%package -n %{libname}
Group:		System/Libraries
Summary: 	GNOME bluetooth library

%description -n %{libname}
Library from GNOME-Bluetooth.

%package -n %{girname}
Group:		System/Libraries
Summary:	GObject Introspection interface for %{name}
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface for %{name}.

%package -n %{develname}
Group:		Development/C
Summary:	Development files and header files from %{name}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libgnomebt3.34-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Development files and header files from %{name}.

%prep
%setup -q -n gnome-bluetooth-%{version}
%autopatch -p1

%build
%meson          \
	-Dgtk_doc=true
	
%meson_build

%install
%meson_install

# Remove files that conflicting with gnome-bluetooth current
rm $RPM_BUILD_ROOT/%{_bindir}/bluetooth-sendto \
  $RPM_BUILD_ROOT/%{_datadir}/applications/bluetooth-sendto.desktop \
  $RPM_BUILD_ROOT/%{_mandir}/man1/bluetooth-sendto.1*

mkdir -p %{buildroot}%{_udevrulesdir}
install %{SOURCE1} %{buildroot}%{_udevrulesdir}/

%find_lang %{name}2 --all-name --with-gnome

# Remove .la files
find %{buildroot} -name "*.la" -exec rm -rf {} \;

%files -f %{name}2.lang
%doc README.md AUTHORS
%{_udevrulesdir}/61-gnome-bluetooth-rfkill.rules
#{_bindir}/*
%{_datadir}/%{oname}
#{_mandir}/man1/*
%{_datadir}/icons/hicolor/*/*/*.*

%files -n %{libname}
#{_libdir}/lib%{name}.so.%{major}*
%{_libdir}/libgnome-bluetooth.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/GnomeBluetooth-%{gi_major}.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/%{oname}
%{_includedir}/%{oname}
%{_libdir}/lib%{oname}.so
%{_datadir}/gir-1.0/GnomeBluetooth-%{gi_major}.gir
%{_libdir}/pkgconfig/*.pc
