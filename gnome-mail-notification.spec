%define		rname mail-notification
Summary:	GNOME notification area mail monitor
Summary(pl):	Monitor poczty widoczny w obszarze powiadamiania GNOME
Name:		gnome-%{rname}
Version:	2.0
Release:	4.1
License:	GPL
Group:		X11/Applications
Source0:	http://savannah.nongnu.org/download/mailnotify/%{rname}-%{version}.tar.gz
# Source0-md5:	56ef7401aba1cb27d881fb0f33a3248d
URL:		http://www.nongnu.org/mailnotify/
Patch0:		%{name}-capplet.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-include.patch
Patch3:		%{name}-gmail-properties.patch
Patch4:		%{name}-imapauth.patch
Patch5:		%{name}-evolution26.patch
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 2.0
BuildRequires:	eel-devel >= 2.14.0
BuildRequires:	evolution-devel >= 2.6
BuildRequires:	gmime-devel >= 2.1.0
BuildRequires:	gnet-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.14.0
BuildRequires:	libicu-devel >= 2.6
BuildRequires:	libsoup-devel >= 2.2
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	scrollkeeper
Requires:	gmime >= 2.1.0
Requires:	libgnomeui >= 2.14.0
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
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1

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
	
%find_lang %{rname} --all-name --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%gconf_schema_install mail-notification.schemas

%preun
%gconf_schema_uninstall mail-notification.schemas

%postun
%scrollkeeper_update_postun

%files -f %{rname}.lang
%defattr(644,root,root,755)
%doc NEWS README TODO
%attr(755,root,root) %{_bindir}/mail-notification
%{_datadir}/%{rname}
%{_desktopdir}/*.desktop
%{_libdir}/bonobo/servers/*
%{_omf_dest_dir}/%{rname}
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/mail-notification.schemas
%{_sysconfdir}/sound/events/*
