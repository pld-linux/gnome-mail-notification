%define		rname mail-notification
Summary:	GNOME notification area mail monitor
Summary(pl):	Monitor poczty widoczny w obszarze powiadamiania GNOME
Name:		gnome-%{rname}
Version:	3.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://savannah.nongnu.org/download/mailnotify/%{rname}-%{version}.tar.gz
# Source0-md5:	d19fb5c96a0f54d1b1541fbddf73488e
URL:		http://www.nongnu.org/mailnotify/
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-configure.patch
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 2.0
BuildRequires:	eel-devel >= 2.15.2
BuildRequires:	evolution-devel >= 2.7.3
BuildRequires:	gmime-devel >= 2.1.19
BuildRequires:	gnet-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.15.1
BuildRequires:	libicu-devel >= 2.6
BuildRequires:	libsoup-devel >= 2.2.94
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	scrollkeeper
Requires:	gmime >= 2.1.19
Requires:	libgnomeui >= 2.15.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mail Notification is an icon for the GNOME Notification Area that
informs users if they have new mail. It handles multiple folders
and multiple folder formats.

%description -l pl
Mail Notification to ikona dla obszaru powiadamiania GNOME informuj±ca
u¿ytkowników, czy maj± now± pocztê. Obs³uguje wiele folderów oraz
wiele formatów folderów.

%package -n evolution-plugin-mail-notification
Summary:	Mail Notification plugin for Evolution
Summary(pl):	Wtyczka Mail Notification dla Evolution
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	evolution >= 2.7.3

%description -n evolution-plugin-mail-notification
Evolution mailbox support for Mail Notification.

%description -n evolution-plugin-mail-notification -l pl
Wsparcie dla skrzynek pocztowych Evolution w Mail Notification.

%prep
%setup -q -n %{rname}-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-install \
	--disable-static \
	--with-evolution-source-dir=%{_includedir}/evolution-2.8
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 \
	autostartdir=%{_datadir}/gnome/autostart

rm -f $RPM_BUILD_ROOT%{_libdir}/evolution/2.8/plugins/*.la

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
%{_datadir}/gnome/autostart/mail-notification.desktop
%{_desktopdir}/*.desktop
%{_libdir}/bonobo/servers/*
%{_omf_dest_dir}/%{rname}
%{_pixmapsdir}/*
%{_sysconfdir}/gconf/schemas/mail-notification.schemas

%files -n evolution-plugin-mail-notification
%defattr(644,root,root,755)
%{_libdir}/evolution/2.8/plugins/liborg-gnome-mail-notification.so
%{_libdir}/evolution/2.8/plugins/org-gnome-mail-notification.eplug
