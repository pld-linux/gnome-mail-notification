%define		rname mail-notification
Summary:	GNOME notification area mail monitor
Summary(pl):	Monitor poczty widoczny w obszarze powiadamiania GNOME
Name:		gnome-%{rname}
Version:	0.3.1
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://savannah.nongnu.org/download/mailnotify/mailnotify.pkg/%{version}/%{rname}-%{version}.tar.gz
# Source0-md5:	a3a10c4a7942a9a11a4cd026d15edf24
URL:		http://www.nongnu.org/mailnotify/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gnet-devel
BuildRequires:	gnome-panel-devel >= 2.0.0
BuildRequires:	pkgconfig
Requires(post): GConf2 >= 2.4.0
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

%build
rm -f missing
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure
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
%gconf_schema_install

%files -f %{rname}.lang
%defattr(644,root,root,755)
%doc NEWS README TODO ChangeLog
%attr(755,root,root) %{_bindir}/mail-notification
%config %{_sysconfdir}/gconf/schemas/*
%{_pixmapsdir}/*
%{_desktopdir}/*.desktop
