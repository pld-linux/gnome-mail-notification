Summary:	GNOME notification area mail monitor
Summary(pl):	Monitor poczty widoczny w obszarze powiadomieñ GNOME
Name:		gnome-mail-notification
Version:	0.3.0
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://savannah.nongnu.org/download/mailnotify/mailnotify.pkg/%{version}/mail-notification-%{version}.tar.gz
# Source0-md5:	3a92381cb74a9b10ea8df9867e670a9c
URL:		http://www.nongnu.org/mailnotify/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gnet-devel
BuildRequires:	gnome-panel-devel >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/gconf

%description
Mail Notification is an icon for the GNOME Notification Area that
informs users if they have new mail. It handles multiple folders
and multiple folder formats.

%description -l pl
Mail Notification to ikona dla Obszaru Powiadomieñ GNOME informuj±ca
u¿ytkowników, czy maj± now± pocztê. Obs³uguje wiele folderów oraz
wiele formatów folderów.

%prep
%setup -q -n mail-notification-%{version}

%build
rm -f missing
%{__autoconf}
%configure \
	--sysconfdir=/etc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang mail-notification

%clean
rm -rf $RPM_BUILD_ROOT

%files -f mail-notification.lang
%defattr(644,root,root,755)
%doc NEWS README TODO ChangeLog
%attr(755,root,root) %{_bindir}/mail-notification
%{_sysconfdir}/schemas/*
%{_pixmapsdir}/*
%{_datadir}/applications/mail-notification.desktop
