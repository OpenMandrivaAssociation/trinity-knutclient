%bcond clang 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg knutclient
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	0.9.5
Release:	%{?tde_version:%{tde_version}_}3
Summary:	A TDE GUI that displays UPS statistics from NUT's upsd [Trinity]
Group:		Applications/Utilities
URL:		http://www.knut.noveradsl.cz/knutclient/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/utilities/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)


BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
KNutClient monitors UPS statistics through the NUT (Network UPS Tools,
http://www.networkupstools.org/) framework on Linux and other systems. This
information, presented in a nice visual format, can be invaluable on
stations using an UPS.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}

# Move desktop icon to XDG directory
if [ -d "%{buildroot}%{tde_prefix}/share/applnk" ]; then
  %__mkdir_p %{buildroot}%{tde_prefix}/share/applications/tde
  %__mv "%{buildroot}%{tde_prefix}/share/applnk/Utilities/knutclient.desktop" "%{buildroot}%{tde_prefix}/share/applications/tde/%{tde_pkg}.desktop"
  %__rm -r "%{buildroot}%{tde_prefix}/share/applnk"
fi

# Links duplicate files
%fdupes "%{?buildroot}%{tde_prefix}/share"


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README.md
%{tde_prefix}/bin/knutclient
%{tde_prefix}/share/applications/tde/knutclient.desktop
%{tde_prefix}/share/apps/knutclient/
%{tde_prefix}/share/doc/tde/HTML/cs/knutclient
%{tde_prefix}/share/doc/tde/HTML/en/knutclient
%{tde_prefix}/share/icons/hicolor/*/apps/*.png
%{tde_prefix}/share/icons/locolor/*/apps/*.png
%{tde_prefix}/share/man/man1/*.1*

