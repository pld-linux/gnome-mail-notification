Summary:	GNOME notification area mail monitor
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
BuildRequires:	gnome-panel-devel >= 2.0.0
BuildRequires:	gnet-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/gconf

%description
Mail Notification is an icon for the GNOME Notification Area that informs users
if they have new mail. It handles multiple folders and multiple folder formats.

%prep
%setup -q -n mail-notification-%{version}

%build
rm -f missing
%{__autoconf}
%configure --sysconfdir=/etc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README TODO ChangeLog
%{_sysconfdir}/schemas/*
%{_pixmapsdir}/*
%{_datadir}/applications/mail-notification.desktop
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/mail-notification.mo
%attr(755,root,root) %{_bindir}/mail-notification
