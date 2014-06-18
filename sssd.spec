# TODO
# - pac-responder (currently relies on MIT krb5 >= 1.9)
# - fix stripping before rpm:
#   *** WARNING: no sources found for /usr/lib64/libipa_hbac.so.0.0.0 (stripped without sourcefile information?)
%define		ldb_version 1.1.0
Summary:	System Security Services Daemon
Summary(pl.UTF-8):	System Security Services Daemon - demon usług bezpieczeństwa systemu
Name:		sssd
Version:	1.11.4
Release:	0.1
License:	GPL v3+
Group:		Applications/System
Source0:	https://fedorahosted.org/released/sssd/%{name}-%{version}.tar.gz
# Source0-md5:	6b52a62fd6f6b170553d032deb7b0bc8
Source1:	%{name}.init
Patch0:		%{name}-python-config.patch
Patch1:		%{name}-heimdal.patch
URL:		https://fedorahosted.org/sssd/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
# nsupdate utility
BuildRequires:	bind-utils
BuildRequires:	c-ares-devel
BuildRequires:	check-devel >= 0.9.5
BuildRequires:	cmocka-devel
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	dbus-devel >= 1.0.0
BuildRequires:	docbook-dtd44-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
BuildRequires:	gettext-devel >= 0.14
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	heimdal-devel
BuildRequires:	keyutils-devel
BuildRequires:	libcollection-devel >= 0.5.1
BuildRequires:	libdhash-devel >= 0.4.2
BuildRequires:	libini_config-devel >= 1.0.0
BuildRequires:	ldb-devel >= %{ldb_version}
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	libselinux-devel
BuildRequires:	libsemanage-devel
BuildRequires:	libtool
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	m4
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel >= 7
BuildRequires:	po4a
BuildRequires:	popt-devel
BuildRequires:	python-devel >= 2.4
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	samba-devel >= 4
BuildRequires:	systemd-units
BuildRequires:	talloc-devel
BuildRequires:	tdb-devel >= 1.1.3
BuildRequires:	tevent-devel
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-client = %{version}-%{release}
Requires:	cyrus-sasl-gssapi
Requires:	ldb >= %{ldb_version}
Requires:	libsss_idmap = %{version}-%{release}
Requires:	rc-scripts >= 0.4.0.10
Requires:	tdb >= 1.1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sssdstatedir		%{_localstatedir}/lib/sss
%define		dbpath			%{sssdstatedir}/db
%define		pipepath		%{sssdstatedir}/pipes
%define		pubconfpath		%{sssdstatedir}/pubconf

# Determine the location of the LDB modules directory
%define		ldb_modulesdir	%(pkg-config --variable=modulesdir ldb)

%description
Provides a set of daemons to manage access to remote directories and
authentication mechanisms. It provides an NSS and PAM interface toward
the system and a pluggable backend system to connect to multiple
different account sources. It is also the basis to provide client
auditing and policy services for projects like FreeIPA.

%description -l pl.UTF-8
Ten pakiet dostarcza zbiór demonów do zarządzania dostępem do zdalnych
katalogów i mechanizmów uwierzytelniania. Udostępnia interfejsy NSS i
PAM dla systemu oraz system backendu z wtyczkami w celu łączenia się z
wieloma różnymi źródłami kont. Jest także podstawą zapewniającą audyt
klientów oraz usługi polityk dla projektów takich jak FreeIPA.

%package client
Summary:	SSSD Client libraries for NSS and PAM
Summary(pl.UTF-8):	Biblioteki klienckie SSSD dla NSS i PAM
License:	LGPL v3+
Group:		Applications/System

%description client
Provides the libraries needed by the PAM and NSS stacks to connect to
the SSSD service.

%description client -l pl.UTF-8
Ten pakiet dostarcza biblioteki wymagane przez stosy PAM i NSS w celu
łączenia się z usługą SSSD.

%package tools
Summary:	Userspace tools for use with the SSSD
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika do używania z SSSD
License:	GPL v3+
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description tools
Provides userspace tools for manipulating users, groups, and nested
groups in SSSD when using id_provider = local in /etc/sssd/sssd.conf.

Also provides several other administrative tools:
 - sss_debuglevel to change the debug level on the fly,
 - sss_seed which pre-creates a user entry for use in kickstarts,
 - sss_obfuscate for generating an obfuscated LDAP password.

%description tools -l pl.UTF-8
Ten pakiet dostarcza narzędzia przestrzeni poleceń do operowania na
użytkownikach, grupach oraz zagnieżdżonych grupach w SSSD w przypadku
używania id_provider = local w /etc/sssd/sssd.conf.

Pakiet zawiera także kilka innych narzędzi administracyjnych:
 - sss_debuglevel do zmiany poziomu diagnostyki w locie,
 - sss_seed tworzący wpis użytkownika do szybkiego rozruchu,
 - sss_obfuscate do generowania utajnionego hasła LDAP.

%package -n libipa_hbac
Summary:	FreeIPA HBAC Evaluator library
Summary(pl.UTF-8):	Biblioteka oceniająca FreeIPA HBAC
License:	LGPL v3+
Group:		Libraries

%description -n libipa_hbac
Utility library to validate FreeIPA HBAC rules for authorization
requests.

%description -n libipa_hbac
Biblioteka narzędziowa do sprawdzania poprawności reguł FreeIPA HBAC
dla żądań autoryzacji.

%package -n libipa_hbac-devel
Summary:	Development files for FreeIPA HBAC Evaluator library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki oceniająca FreeIPA HBAC
License:	LGPL v3+
Group:		Development/Libraries
Requires:	libipa_hbac = %{version}-%{release}

%description -n libipa_hbac-devel
Development files for FreeIPA HBAC Evaluator library.

%description -n libipa_hbac-devel -l pl.UTF-8
Pliki programistyczne biblioteki oceniająca FreeIPA HBAC.

%package -n python-libipa_hbac
Summary:	Python bindings for the FreeIPA HBAC Evaluator library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki oceniającej FreeIPA HBAC
License:	LGPL v3+
Group:		Libraries/Python
Requires:	libipa_hbac = %{version}-%{release}
Obsoletes:	libipa_hbac-python

%description -n python-libipa_hbac
This package contains the bindings so that libipa_hbac can be used by
Python applications.

%description -n python-libipa_hbac -l pl.UTF-8
Ten pakiet zawiera wiązania pozwalające na używanie libipa_hbac w
aplikacjach Pythona.

%package -n libsss_idmap
Summary:	FreeIPA Idmap library
Summary(pl.UTF-8):	Biblioteka FreeIPA Idmap
Group:		Libraries
License:	LGPL v3+

%description -n libsss_idmap
Utility library to convert SIDs to Unix uids and gids.

%description -n libsss_idmap -l pl.UTF-8
Biblioteka narzędziowa konwertująca SID-y na uniksowe uidy i gidy.

%package -n libsss_idmap-devel
Summary:	Development files for FreeIPA Idmap library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki FreeIPA Idmap
Group:		Development/Libraries
License:	LGPL v3+
Requires:	libsss_idmap = %{version}-%{release}

%description -n libsss_idmap-devel
Development files for FreeIPA Idmap library.

%description -n libsss_idmap-devel -l pl.UTF-8
Pliki programistyczne biblioteki FreeIPA Idmap.

%package -n libsss_nss_idmap
Summary:	Library for SID based lookups
Summary(pl.UTF-8):	Biblioteka do wyszukiwań w oparciu o SID
Group:		Libraries
License:	LGPL v3+

%description -n libsss_nss_idmap
Utility library for SID based lookups.

%description -n libsss_nss_idmap -l pl.UTF-8
Biblioteka do wyszukiwań w oparciu o SID.

%package -n libsss_nss_idmap-devel
Summary:	Development files for sss_nss_idmap library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki sss_nss_idmap
Group:		Development/Libraries
License:	LGPL v3+
Requires:	libsss_nss_idmap = %{version}-%{release}

%description -n libsss_nss_idmap-devel
Development files for sss_nss_idmap library.

%description -n libsss_nss_idmap-devel -l pl.UTF-8
Pliki programistyczne biblioteki sss_nss_idmap.

%package -n python-libsss_nss_idmap
Summary:	Python bindings for libsss_nss_idmap
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libsss_nss_idmap
Group:		Libraries/Python
License:	LGPL v3+
Requires:	libsss_nss_idmap = %{version}-%{release}

%description -n python-libsss_nss_idmap
This package contains the bindings so that libsss_nss_idmap can be
used by Python applications.

%description -n python-libsss_nss_idmap -l pl.UTF-8
Ten pakiet zawiera wiązania umożliwiające korzystanie z biblioteki
libsss_nss_idmap w aplikacjach Pythona.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__gettextize}
%{__aclocal}
%{__automake}
%{__autoconf}
#CFLAGS="-Wno-deprecated-declarations"
%configure \
	NSCD=/usr/sbin/nscd \
	--with-db-path=%{dbpath} \
	--with-pipe-path=%{pipepath} \
	--with-pubconf-path=%{pubconfpath} \
	--with-init-dir=%{_initrddir} \
	--enable-nsslibdir=/%{_lib} \
	--enable-pammoddir=/%{_lib}/security \
	--disable-rpath \
	--with-test-dir=/dev/shm

%{__make}

%if %{with tests}
export CK_TIMEOUT_MULTIPLIER=10
%{__make} check
unset CK_TIMEOUT_MULTIPLIER
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Prepare language files
%find_lang %{name}

# Copy default sssd.conf file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sssd/sssd.api.d
cp -p src/examples/sssd-example.conf $RPM_BUILD_ROOT%{_sysconfdir}/sssd/sssd.conf

# Copy default logrotate file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
cp -p src/examples/logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sssd

# Make sure SSSD is able to run on read-only root
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d
cp -p src/examples/rwtab $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/sssd

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

# Remove .la files created by libtool
%{__rm} \
	$RPM_BUILD_ROOT/%{_lib}/libnss_sss.la \
	$RPM_BUILD_ROOT/%{_lib}/security/pam_sss.la \
	$RPM_BUILD_ROOT%{ldb_modulesdir}/memberof.la \
	$RPM_BUILD_ROOT%{_libdir}/krb5/plugins/libkrb5/sss*.la \
	$RPM_BUILD_ROOT%{_libdir}/sssd/libsss_*.la \
	$RPM_BUILD_ROOT%{_libdir}/sssd/modules/libsss_*.la \
	$RPM_BUILD_ROOT%{_libdir}/lib*.la \
	$RPM_BUILD_ROOT%{py_sitedir}/*.la

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

echo '%%defattr(644,root,root,755)' > sssd_client.lang
echo '%%defattr(644,root,root,755)' > sssd_tools.lang
for man in $(find $RPM_BUILD_ROOT%{_mandir}/??/man? -type f | sed -e "s#$RPM_BUILD_ROOT%{_mandir}/##"); do
	lang=$(echo $man | cut -c 1-2)
	case $(basename $man) in
	pam_sss.8|sssd_krb5_locator_plugin.8)
		echo "%lang(${lang}) %{_mandir}/${man}*" >> sssd_client.lang
		;;
	sss_debuglevel.8|sss_group*.8|sss_obfuscate.8|sss_seed.8|sss_user*.8)
		echo "%lang(${lang}) %{_mandir}/${man}*" >> sssd_tools.lang
		;;
	*)
		echo "%lang(${lang}) %{_mandir}/${man}*" >> sssd.lang
		;;
	esac
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun	-p /sbin/ldconfig

%post	client -p /sbin/ldconfig
%postun	client -p /sbin/ldconfig

%post	-n libipa_hbac -p /sbin/ldconfig
%postun	-n libipa_hbac -p /sbin/ldconfig

%post	-n libsss_idmap -p /sbin/ldconfig
%postun	-n libsss_idmap -p /sbin/ldconfig

%post	-n libsss_nss_idmap -p /sbin/ldconfig
%postun	-n libsss_nss_idmap -p /sbin/ldconfig

%files -f sssd.lang
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/sssd
%attr(755,root,root) %{_bindir}/sss_ssh_authorizedkeys
%attr(755,root,root) %{_bindir}/sss_ssh_knownhostsproxy
%attr(755,root,root) %{_sbindir}/sss_cache
%attr(755,root,root) %{_sbindir}/sssd
%attr(755,root,root) %{_libdir}/libsss_sudo.so
%dir %{_libdir}/sssd
# internal shared libraries
%attr(755,root,root) %{_libdir}/sssd/libsss_child.so
%attr(755,root,root) %{_libdir}/sssd/libsss_crypt.so
%attr(755,root,root) %{_libdir}/sssd/libsss_debug.so
%attr(755,root,root) %{_libdir}/sssd/libsss_ldap_common.so
%attr(755,root,root) %{_libdir}/sssd/libsss_util.so
# modules
%attr(755,root,root) %{_libdir}/sssd/libsss_simple.so
%attr(755,root,root) %{_libdir}/sssd/libsss_ad.so
%attr(755,root,root) %{_libdir}/sssd/libsss_ipa.so
%attr(755,root,root) %{_libdir}/sssd/libsss_krb5.so
%attr(755,root,root) %{_libdir}/sssd/libsss_krb5_common.so
%attr(755,root,root) %{_libdir}/sssd/libsss_ldap.so
%attr(755,root,root) %{_libdir}/sssd/libsss_proxy.so
%dir %{_libdir}/sssd/modules
%attr(755,root,root) %{_libdir}/sssd/modules/libsss_autofs.so
%if "%{_libdir}" != "%{_libexecdir}"
%dir %{_libexecdir}/sssd
%endif
%attr(755,root,root) %{_libexecdir}/sssd/krb5_child
%attr(755,root,root) %{_libexecdir}/sssd/ldap_child
%attr(755,root,root) %{_libexecdir}/sssd/proxy_child
%attr(755,root,root) %{_libexecdir}/sssd/sssd_autofs
%attr(755,root,root) %{_libexecdir}/sssd/sssd_be
%attr(755,root,root) %{_libexecdir}/sssd/sssd_nss
%attr(755,root,root) %{_libexecdir}/sssd/sssd_pam
%attr(755,root,root) %{_libexecdir}/sssd/sssd_ssh
%attr(755,root,root) %{_libexecdir}/sssd/sssd_sudo
%dir %{_datadir}/sssd
%{_datadir}/sssd/sssd.api.conf
%dir %{_datadir}/sssd/sssd.api.d
%{_datadir}/sssd/sssd.api.d/sssd-ad.conf
%{_datadir}/sssd/sssd.api.d/sssd-ipa.conf
%{_datadir}/sssd/sssd.api.d/sssd-krb5.conf
%{_datadir}/sssd/sssd.api.d/sssd-ldap.conf
%{_datadir}/sssd/sssd.api.d/sssd-local.conf
%{_datadir}/sssd/sssd.api.d/sssd-proxy.conf
%{_datadir}/sssd/sssd.api.d/sssd-simple.conf
%attr(755,root,root) %{ldb_modulesdir}/memberof.so
%dir %{sssdstatedir}
%attr(700,root,root) %dir %{dbpath}
%dir %{pipepath}
%dir %{pubconfpath}
%attr(700,root,root) %dir %{pipepath}/private
%attr(750,root,root) %dir %{_var}/log/%{name}
%attr(700,root,root) %dir %{_sysconfdir}/sssd
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sssd/sssd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/sssd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rwtab.d/sssd
%{_mandir}/man1/sss_ssh_authorizedkeys.1*
%{_mandir}/man1/sss_ssh_knownhostsproxy.1*
%{_mandir}/man5/sssd.conf.5*
%{_mandir}/man5/sssd-ad.5*
%{_mandir}/man5/sssd-ipa.5*
%{_mandir}/man5/sssd-krb5.5*
%{_mandir}/man5/sssd-ldap.5*
%{_mandir}/man5/sssd-simple.5*
%{_mandir}/man5/sssd-sudo.5*
%{_mandir}/man8/sss_cache.8*
%{_mandir}/man8/sssd.8*
%attr(755,root,root) %{py_sitedir}/pysss.so
%attr(755,root,root) %{py_sitedir}/pysss_murmur.so
%dir %{py_sitescriptdir}/SSSDConfig
%{py_sitescriptdir}/SSSDConfig/*.py[co]
%{py_sitescriptdir}/SSSDConfig-%{version}-py*.egg-info

%files client -f sssd_client.lang
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_sss.so.2
%attr(755,root,root) /%{_lib}/security/pam_sss.so
# FIXME: is it proper path for heimdal? where to package parent dirs?
#%attr(755,root,root) %{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%{_mandir}/man8/pam_sss.8*
%{_mandir}/man8/sssd_krb5_locator_plugin.8*

%files tools -f sssd_tools.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/sss_debuglevel
%attr(755,root,root) %{_sbindir}/sss_groupadd
%attr(755,root,root) %{_sbindir}/sss_groupdel
%attr(755,root,root) %{_sbindir}/sss_groupmod
%attr(755,root,root) %{_sbindir}/sss_groupshow
%attr(755,root,root) %{_sbindir}/sss_obfuscate
%attr(755,root,root) %{_sbindir}/sss_seed
%attr(755,root,root) %{_sbindir}/sss_useradd
%attr(755,root,root) %{_sbindir}/sss_userdel
%attr(755,root,root) %{_sbindir}/sss_usermod
%{_mandir}/man8/sss_debuglevel.8*
%{_mandir}/man8/sss_groupadd.8*
%{_mandir}/man8/sss_groupdel.8*
%{_mandir}/man8/sss_groupmod.8*
%{_mandir}/man8/sss_groupshow.8*
%{_mandir}/man8/sss_obfuscate.8*
%{_mandir}/man8/sss_seed.8*
%{_mandir}/man8/sss_useradd.8*
%{_mandir}/man8/sss_userdel.8*
%{_mandir}/man8/sss_usermod.8*

%files -n libipa_hbac
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipa_hbac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libipa_hbac.so.0

%files -n libipa_hbac-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipa_hbac.so
%{_includedir}/ipa_hbac.h
%{_pkgconfigdir}/ipa_hbac.pc

%files -n python-libipa_hbac
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pyhbac.so

%files -n libsss_idmap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsss_idmap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsss_idmap.so.0

%files -n libsss_idmap-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsss_idmap.so
%{_includedir}/sss_idmap.h
%{_pkgconfigdir}/sss_idmap.pc

%files -n libsss_nss_idmap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsss_nss_idmap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsss_nss_idmap.so.0

%files -n libsss_nss_idmap-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsss_nss_idmap.so
%{_includedir}/sss_nss_idmap.h
%{_pkgconfigdir}/sss_nss_idmap.pc

%files -n python-libsss_nss_idmap
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pysss_nsss_idmap.so
