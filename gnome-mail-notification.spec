%define		rname mail-notification
Summary:	GNOME notification area mail monitor
Summary(pl):	Monitor poczty widoczny w obszarze powiadamiania GNOME
Name:		gnome-%{rname}
Version:	1.1
Release:	3
License:	GPL
Group:		X11/Applications
Source0:	http://savannah.nongnu.org/download/mailnotify/%{rname}-%{version}.tar.gz
# Source0-md5:	2359fb53128b12cf295bdf8553e5869b
URL:		http://www.nongnu.org/mailnotify/
Patch0:		%{name}-capplet.patch
Patch1:		%{name}-desktop.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 2.0
BuildRequires:	gmime-devel >= 2.1.0
BuildRequires:	gnet-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	eel-devel >= 2.10.0
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires: rpmbuild(macros) >= 1.196
Requires(post,preun):	GConf2 >= 2.10.0
Requires(post,postun):	scrollkeeper
Requires:	gmime >= 2.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mail Notification is an icon for the GNOME Notification Area that
informs users if they have new mail. It handles multiple folders
and multiple folder formats.

%description -l pl
Mail Notification to ikona dla obszaru powiadamiania GNOME informuj±ca
u¿ytkowników, czy maj± now± pocztê. Obs³uguje wiele folderów oraz
wiele formatów folderów.

%prep
%setup -q -n %{rname}-%{version}
%patch0 -p0
%patch1 -p1

%build
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
	
mv $RPM_BUILD_ROOT%{_datadir}/control-center-2.0/capplets/mail-notification-properties.desktop $RPM_BUILD_ROOT%{_desktopdir}

%find_lang %{rname} --all-name --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/scrollkeeper-update -q
%gconf_schema_install /etc/gconf/schemas/mail-notification.schemas

%preun
if [ $1 = 0 ]; then
	%gconf_schema_uninstall /etc/gconf/schemas/mail-notification.schemas
fi

%postun
if [ $1 = 0 ]; then
	/usr/bin/scrollkeeper-update -q
fi

%files -f %{rname}.lang
%defattr(644,root,root,755)
%doc NEWS README TODO
%attr(755,root,root) %{_bindir}/mail-notification
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/%{rname}
%{_pixmapsdir}/*
%{_desktopdir}/*.desktop
%{_omf_dest_dir}/%{rname}
%{_libdir}/bonobo/servers/*
%{_sysconfdir}/sound/events/*
