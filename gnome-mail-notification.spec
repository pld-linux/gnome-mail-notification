%define		rname mail-notification
Summary:	GNOME notification area mail monitor
Summary(pl.UTF-8):	Monitor poczty widoczny w obszarze powiadamiania GNOME
Name:		gnome-mail-notification
Version:	5.4
Release:	25
License:	GPL v3+
Group:		X11/Applications
Source0:	https://github.com/epienbroek/mail-notification/tarball/master/%{rname}-%{version}.tar.gz
# Source0-md5:	1c4aea14dd2f9b89b659eaf39cde05f4
Patch0:		mail-notification-jb-gcc-format.patch
Patch1:		jb-glibc-2.19.patch
Patch2:		jb-evolution-plugin-detect.patch
Patch3:		evolution-3.12.patch
Patch4:		evolution-3.16.patch
URL:		http://www.nongnu.org/mailnotify/
BuildRequires:	GConf2-devel >= 2.22.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 2.0
BuildRequires:	evolution-devel >= 3.0.0
BuildRequires:	gettext-tools
BuildRequires:	gmime-devel >= 2.1.19
BuildRequires:	gmime22-devel
BuildRequires:	gnome-vfs2-devel >= 2.22.0
BuildRequires:	gob2 >= 2.0.17
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	intltool >= 0.36.2
BuildRequires:	libbonobo-devel >= 2.22.0
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libgnome-keyring-devel >= 3.0.0
BuildRequires:	libgnomeui-devel >= 2.22.01
BuildRequires:	libnotify-devel >= 0.4.1
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	nautilus-devel >= 2.30
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
BuildRequires:	sed >= 4.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	gmime >= 2.1.19
Requires:	libgnomeui >= 2.22.01
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mail Notification is an icon for the GNOME Notification Area that
informs users if they have new mail. It handles multiple folders and
multiple folder formats.

%description -l pl.UTF-8
Mail Notification to ikona dla obszaru powiadamiania GNOME informująca
użytkowników, czy mają nową pocztę. Obsługuje wiele folderów oraz
wiele formatów folderów.

%package -n evolution-plugin-mail-notification
Summary:	Mail Notification plugin for Evolution
Summary(pl.UTF-8):	Wtyczka Mail Notification dla Evolution
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	evolution >= 3.0.0

%description -n evolution-plugin-mail-notification
Evolution mailbox support for Mail Notification.

%description -n evolution-plugin-mail-notification -l pl.UTF-8
Wsparcie dla skrzynek pocztowych Evolution w Mail Notification.

%prep
%setup -q -n epienbroek-%{rname}-45d11d2
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

%build
./jb configure \
	cflags="%{rpmcflags}" \
	cppflags="%{rpmcppflags}" \
	ldflags="%{rpmldflags}" \
	prefix=%{_prefix} \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir} \
	datadir=%{_datadir} \
	libdir=%{_libdir} \
	libexecdir=%{_libexecdir} \
	localstatedir=%{_localstatedir} \
	libs="-lX11" \
	destdir=$RPM_BUILD_ROOT \
	install-gconf-schemas=no \
	evolution-plugin-dir=%{_libdir}/evolution/plugins/

./jb build

%install
rm -rf $RPM_BUILD_ROOT

./jb install

# install also GtkBuilder files
#cp -p ui/mailbox-properties-dialog.ui $RPM_BUILD_ROOT%{_datadir}/mail-notification
#cp -p ui/properties-dialog.ui $RPM_BUILD_ROOT%{_datadir}/mail-notification

%find_lang %{rname} --all-name --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%gconf_schema_install mail-notification.schemas
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall mail-notification.schemas

%postun
%scrollkeeper_update_postun
%update_icon_cache hicolor

%files -f %{rname}.lang
%defattr(644,root,root,755)
%doc NEWS README TODO
%attr(755,root,root) %{_bindir}/mail-notification
%{_datadir}/mail-notification
%{_sysconfdir}/xdg/autostart/mail-notification.desktop
%{_desktopdir}/mail-notification-properties.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_sysconfdir}/gconf/schemas/mail-notification.schemas

%files -n evolution-plugin-mail-notification
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/evolution/plugins/liborg-jylefort-mail-notification.so
%{_libdir}/evolution/plugins/org-jylefort-mail-notification.eplug
