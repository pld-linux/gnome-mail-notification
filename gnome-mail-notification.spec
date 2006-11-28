%define		rname mail-notification
Summary:	GNOME notification area mail monitor
Summary(pl):	Monitor poczty widoczny w obszarze powiadamiania GNOME
Name:		gnome-%{rname}
Version:	4.0
%define pre rc1
Release:	0.%{pre}.1
License:	GPL
Group:		X11/Applications
Source0:	http://savannah.nongnu.org/download/mailnotify/%{rname}-%{version}-%{pre}.tar.gz
# Source0-md5:	91c09b72a59d161564b47fff033be37e
URL:		http://www.nongnu.org/mailnotify/
Patch0:		%{name}-desktop.patch
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 2.0
BuildRequires:	eel-devel >= 2.14.1
BuildRequires:	evolution-devel >= 2.8.0
BuildRequires:	gmime-devel >= 2.1.19
BuildRequires:	gnet-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.14.1
BuildRequires:	libicu-devel >= 2.6
BuildRequires:	libnotify-devel
BuildRequires:	libsoup-devel >= 2.2.7
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	scrollkeeper
Requires:	gmime >= 2.1.19
Requires:	libgnomeui >= 2.14.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mail Notification is an icon for the GNOME Notification Area that
informs users if they have new mail. It handles multiple folders
and multiple folder formats.

%description -l pl
Mail Notification to ikona dla obszaru powiadamiania GNOME informuj�ca
u�ytkownik�w, czy maj� now� poczt�. Obs�uguje wiele folder�w oraz
wiele format�w folder�w.

%package -n evolution-plugin-mail-notification
Summary:	Mail Notification plugin for Evolution
Summary(pl):	Wtyczka Mail Notification dla Evolution
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	evolution >= 2.8.0

%description -n evolution-plugin-mail-notification
Evolution mailbox support for Mail Notification.

%description -n evolution-plugin-mail-notification -l pl
Wsparcie dla skrzynek pocztowych Evolution w Mail Notification.

%prep
%setup -q -n %{rname}-%{version}-%{pre}
%patch0 -p1

%build
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

rm -f $RPM_BUILD_ROOT%{_libdir}/evolution/2.6/plugins/*.la

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
%{_iconsdir}/*
%{_sysconfdir}/gconf/schemas/mail-notification.schemas

%files -n evolution-plugin-mail-notification
%defattr(644,root,root,755)
%{_libdir}/evolution/2.8/plugins/liborg-gnome-mail-notification.so
%{_libdir}/evolution/2.8/plugins/org-gnome-mail-notification.eplug
