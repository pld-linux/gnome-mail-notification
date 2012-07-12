%define		evo_ver	3.4
%define		rname mail-notification
Summary:	GNOME notification area mail monitor
Summary(pl.UTF-8):	Monitor poczty widoczny w obszarze powiadamiania GNOME
Name:		gnome-mail-notification
Version:	5.4
Release:	14
License:	GPL v3+
Group:		X11/Applications
Source0:	http://savannah.nongnu.org/download/mailnotify/%{rname}-%{version}.tar.bz2
# Source0-md5:	c8dc33a61251acb5474e56eab6b18f43
Patch0:		%{name}-evolution.patch
Patch1:		%{name}-evolution-gtkhtml.patch
Patch3:		%{name}-camel_headers.patch
Patch4:		%{name}-evolution-3-0.patch
Patch5:		%{name}-gtk3-support.patch
Patch6:		%{name}-libemail.patch
URL:		http://www.nongnu.org/mailnotify/
BuildRequires:	GConf2-devel >= 2.22.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel >= 2.0
BuildRequires:	evolution-devel >= 3.0.0
BuildRequires:	gettext-devel
BuildRequires:	gmime-devel >= 2.1.19
BuildRequires:	gmime22-devel
BuildRequires:	libgnome-keyring-devel >= 3.0.0
BuildRequires:	gnome-vfs2-devel >= 2.22.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	intltool >= 0.36.2
BuildRequires:	libbonobo-devel >= 2.22.0
BuildRequires:	libglade2-devel >= 1:2.6.2
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
%setup -q -n %{rname}-%{version}

# Convert the Glade UI to GtkBuilder
cd ui
gtk-builder-convert mailbox-properties-dialog.glade mailbox-properties-dialog.ui
gtk-builder-convert properties-dialog.glade properties-dialog.ui
sed -i s@'<property name="has_separator">False</property>'@@ mailbox-properties-dialog.ui
sed -i s@'<property name="has_separator">False</property>'@@ properties-dialog.ui
cd -

%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p0
%patch6 -p1

%build
./jb configure \
	libs="-lX11" \
	destdir=$RPM_BUILD_ROOT \
	sysconfdir=%{_sysconfdir} \
	localstatedir=%{_var} \
	install-gconf-schemas=no
./jb build

%install
rm -rf $RPM_BUILD_ROOT

./jb install

# install also GtkBuilder files
cp -p ui/mailbox-properties-dialog.ui $RPM_BUILD_ROOT%{_datadir}/mail-notification
cp -p ui/properties-dialog.ui $RPM_BUILD_ROOT%{_datadir}/mail-notification

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
%attr(755,root,root) %{_libdir}/evolution/%{evo_ver}/plugins/liborg-jylefort-mail-notification.so
%{_libdir}/evolution/%{evo_ver}/plugins/org-jylefort-mail-notification.eplug
