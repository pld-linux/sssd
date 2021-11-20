# TODO
# - fix stripping before rpm:
#   *** WARNING: no sources found for /usr/lib64/libipa_hbac.so.0.0.0 (stripped without sourcefile information?)
# - add info how sssd-heimdal.patch is updated, where is it's origin?
#
# Conditional build:
%bcond_with	tests	# check target
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_with	krb5	# MIT Kerberos V instead of Heimdal (enables locator plugin, profile support and pac-responder)

%define		ldb_version 1.1.0
Summary:	System Security Services Daemon
Summary(pl.UTF-8):	System Security Services Daemon - demon usług bezpieczeństwa systemu
Name:		sssd
Version:	1.13.4
Release:	12
License:	GPL v3+
Group:		Applications/System
Source0:	https://fedorahosted.org/released/sssd/%{name}-%{version}.tar.gz
# Source0-md5:	d147e0a4f4719d993693c6a99370b350
Source1:	%{name}.init
Patch0:		%{name}-python.patch
Patch1:		%{name}-heimdal.patch
Patch2:		%{name}-systemd.patch
Patch3:		%{name}-link.patch
Patch4:		format.patch
Patch5:		array-size.patch
Patch6:		samba-4.12.patch
URL:		https://fedorahosted.org/sssd/
BuildRequires:	augeas-devel >= 1.0.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
# nsupdate utility
BuildRequires:	bind-utils
BuildRequires:	c-ares-devel
BuildRequires:	check-devel >= 0.9.5
BuildRequires:	cifs-utils-devel
%{?with_tests:BuildRequires:	cmocka-devel >= 1.0.0}
BuildRequires:	cyrus-sasl-devel >= 2
BuildRequires:	dbus-devel >= 1.0.0
BuildRequires:	docbook-dtd44-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
%{?with_tests:BuildRequires:	fakeroot}
BuildRequires:	gettext-tools >= 0.14.4
BuildRequires:	glib2-devel >= 2.0
%{!?with_krb5:BuildRequires:	heimdal-devel}
BuildRequires:	keyutils-devel
%{?with_krb5:BuildRequires:	krb5-devel >= 1.9}
BuildRequires:	ldb-devel >= %{ldb_version}
BuildRequires:	libcollection-devel >= 0.5.1
BuildRequires:	libdhash-devel >= 0.4.2
BuildRequires:	libini_config-devel >= 1.1.0
BuildRequires:	libltdl-devel
BuildRequires:	libnfsidmap-devel
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	libselinux-devel
BuildRequires:	libsemanage-devel
BuildRequires:	libsmbclient-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	m4
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
%{?with_tests:BuildRequires:	nss_wrapper}
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel >= 7
BuildRequires:	pkgconfig
BuildRequires:	po4a
BuildRequires:	popt-devel
%{?with_python2:BuildRequires:	python-devel >= 1:2.6}
%{?with_tests:BuildRequires:	python-pytest}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.3}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
# pkgconfig(ndr_nbt), pkgconfig(ndr_krb5pac) if with krb5
BuildRequires:	samba-devel >= 4
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	systemd-units
BuildRequires:	talloc-devel
BuildRequires:	tdb-devel >= 1.1.3
BuildRequires:	tevent-devel
%{?with_tests:BuildRequires:	uid_wrapper}
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-client = %{version}-%{release}
Requires:	cyrus-sasl-gssapi
Requires:	ldb >= %{ldb_version}
Requires:	libcollection >= 0.5.1
Requires:	libdhash >= 0.4.2
Requires:	libini_config >= 1.1.0
Requires:	libsss_idmap = %{version}-%{release}
Requires:	pcre >= 7
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
Requires:	libsss_idmap = %{version}-%{release}
Requires:	libsss_nss_idmap = %{version}-%{release}

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

%package -n python-sss
Summary:	Python 2 bindings for sssd
Summary(pl.UTF-8):	Wiązania Pythona 2 do sssd
License:	LGPL v3+
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-sss
Python 2 module for manipulating users, groups, and nested groups in
SSSD when using id_provider = local in /etc/sssd/sssd.conf.

This module also provides several other useful Python 2 bindings:
 - function for retrieving list of groups user belongs to.
 - class for obfuscation of passwords

%description -n python-sss -l pl.UTF-8
Moduł Pythona 2 do operowania na użytkownikach, grupach i
zagnieżdżonych grupach w SSSD w przypadku używania id_provider = local
w /etc/sssd/sssd.conf.

Ten moduł dostarcza także kilka innych przydatnych wiązań Pythona 2:
 - funkcję do użyskiwania list grup, do których należy użytkownik,
 - klasę do ukrywania haseł.

%package -n python-sss-murmur
Summary:	Python 2 bindings for murmur hash function
Summary(pl.UTF-8):	Wiązania Pythona 2 do funkcji mieszającej murmur
License:	LGPL v3+
Group:		Libraries/Python

%description -n python-sss-murmur
Python 2 module for calculating the murmur hash version 3.

%description -n python-sss-murmur -l pl.UTF-8
Moduł Pythona 2 do obliczania skrótu murmur w wersji 3.

%package -n python-sssdconfig
Summary:	SSSD and IPA configuration file manipulation classes and functions for Python 2
Summary(pl.UTF-8):	Klasy i funkcje Pythona 2 do operowania na plikach konfiguracyjnych SSSD oraz IPA
License:	GPL v3+
Group:		Libraries/Python
BuildArch:	noarch

%description -n python-sssdconfig
SSSD and IPA configuration file manipulation classes and functions for
Python 2.

%description -n python-sssdconfig -l pl.UTF-8
Klasy i funkcje Pythona 2 do operowania na plikach konfiguracyjnych
SSSD oraz IPA.

%package -n python3-sss
Summary:	Python 3 bindings for sssd
Summary(pl.UTF-8):	Wiązania Pythona 3 do sssd
License:	LGPL v3+
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-sss
Python 3 module for manipulating users, groups, and nested groups in
SSSD when using id_provider = local in /etc/sssd/sssd.conf.

This module also provides several other useful Python 3 bindings:
 - function for retrieving list of groups user belongs to.
 - class for obfuscation of passwords

%description -n python3-sss -l pl.UTF-8
Moduł Pythona 3 do operowania na użytkownikach, grupach i
zagnieżdżonych grupach w SSSD w przypadku używania id_provider = local
w /etc/sssd/sssd.conf.

Ten moduł dostarcza także kilka innych przydatnych wiązań Pythona 3:
 - funkcję do użyskiwania list grup, do których należy użytkownik,
 - klasę do ukrywania haseł.

%package -n python3-sss-murmur
Summary:	Python 3 bindings for murmur hash function
Summary(pl.UTF-8):	Wiązania Pythona 3 do funkcji mieszającej murmur
License:	LGPL v3+
Group:		Libraries/Python

%description -n python3-sss-murmur
Python 3 module for calculating the murmur hash version 3.

%description -n python3-sss-murmur -l pl.UTF-8
Moduł Pythona 3 do obliczania skrótu murmur w wersji 3.

%package -n python3-sssdconfig
Summary:	SSSD and IPA configuration file manipulation classes and functions for Python 3
Summary(pl.UTF-8):	Klasy i funkcje Pythona 3 do operowania na plikach konfiguracyjnych SSSD oraz IPA
License:	GPL v3+
Group:		Libraries/Python
BuildArch:	noarch

%description -n python3-sssdconfig
SSSD and IPA configuration file manipulation classes and functions for
Python 3.

%description -n python3-sssdconfig -l pl.UTF-8
Klasy i funkcje Pythona 3 do operowania na plikach konfiguracyjnych
SSSD oraz IPA.

%package libwbclient
Summary:	The SSSD libwbclient implementation
Summary(pl.UTF-8):	Implementacja libwbclient oparta na SSSD
Group:		Libraries
License:	LGPL v3+
Requires:	libsss_nss_idmap = %{version}-%{release}

%description libwbclient
The SSSD implementation of Samba wbclient library.

%description libwbclient -l pl.UTF-8
Implementacja biblioteki Samba wbclient oparta na SSSD.

%package libwbclient-devel
Summary:	Development files of the SSSD libwbclient implementation
Summary(pl.UTF-8):	Pliki programistyczne implementacja libwbclient oparta na SSSD
Group:		Development/Libraries
License:	LGPL v3+
Requires:	%{name}-libwbclient = %{version}-%{release}

%description libwbclient-devel
Development files for the SSSD implementation of Samba wbclient
library.

%description libwbclient-devel -l pl.UTF-8
Pliki programistyczne implementacji biblioteki Samba wbclient opartej
na SSSD.

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
Summary:	Python 2 bindings for the FreeIPA HBAC Evaluator library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki oceniającej FreeIPA HBAC
License:	LGPL v3+
Group:		Libraries/Python
Requires:	libipa_hbac = %{version}-%{release}
Obsoletes:	libipa_hbac-python

%description -n python-libipa_hbac
This package contains the bindings so that libipa_hbac can be used by
Python 2 applications.

%description -n python-libipa_hbac -l pl.UTF-8
Ten pakiet zawiera wiązania pozwalające na używanie libipa_hbac w
aplikacjach Pythona 2.

%package -n python3-libipa_hbac
Summary:	Python 3 bindings for the FreeIPA HBAC Evaluator library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki oceniającej FreeIPA HBAC
License:	LGPL v3+
Group:		Libraries/Python
Requires:	libipa_hbac = %{version}-%{release}

%description -n python3-libipa_hbac
This package contains the bindings so that libipa_hbac can be used by
Python 3 applications.

%description -n python3-libipa_hbac -l pl.UTF-8
Ten pakiet zawiera wiązania pozwalające na używanie libipa_hbac w
aplikacjach Pythona 3.

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
Summary:	Python 2 bindings for libsss_nss_idmap
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki libsss_nss_idmap
Group:		Libraries/Python
License:	LGPL v3+
Requires:	libsss_nss_idmap = %{version}-%{release}

%description -n python-libsss_nss_idmap
This package contains the bindings so that libsss_nss_idmap can be
used by Python 2 applications.

%description -n python-libsss_nss_idmap -l pl.UTF-8
Ten pakiet zawiera wiązania umożliwiające korzystanie z biblioteki
libsss_nss_idmap w aplikacjach Pythona 2.

%package -n python3-libsss_nss_idmap
Summary:	Python 3 bindings for libsss_nss_idmap
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libsss_nss_idmap
Group:		Libraries/Python
License:	LGPL v3+
Requires:	libsss_nss_idmap = %{version}-%{release}

%description -n python3-libsss_nss_idmap
This package contains the bindings so that libsss_nss_idmap can be
used by Python 3 applications.

%description -n python3-libsss_nss_idmap -l pl.UTF-8
Ten pakiet zawiera wiązania umożliwiające korzystanie z biblioteki
libsss_nss_idmap w aplikacjach Pythona 3.

%package -n libsss_simpleifp
Summary:	A library that simplifies work with the InfoPipe responder
Summary(pl.UTF-8):	Biblioteka upraszczająca pracę z responderem InfoPipe
Group:		Libraries
Requires:	dbus-libs >= 1.0.0
Requires:	libdhash >= 0.4.2

%description -n libsss_simpleifp
A library that simplifies work with the InfoPipe responder.

%description -n libsss_simpleifp -l pl.UTF-8
Biblioteka upraszczająca pracę z responderem InfoPipe.

%package -n libsss_simpleifp-devel
Summary:	Header files for libsss_simpleifp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsss_simpleifp
Group:		Development/Libraries
Requires:	dbus-devel >= 1.0.0
Requires:	libdhash-devel >= 0.4.2
Requires:	libsss_simpleifp = %{version}-%{release}

%description -n libsss_simpleifp-devel
Header files for libsss_simpleifp library.

%description -n libsss_simpleifp-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsss_simpleifp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/python(\s|$),#!%{__python}\1,' \
      src/tools/sss_obfuscate

%build
%{__libtoolize}
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	NSCD=/usr/sbin/nscd \
	%{!?with_krb5:--disable-krb5-locator-plugin} \
	--enable-nfsidmaplibdir=/%{_lib}/libnfsidmap \
	--enable-nsslibdir=/%{_lib} \
	%{!?with_krb5:--disable-pac-responder} \
	--enable-pammoddir=/%{_lib}/security \
	--disable-rpath \
	--with-db-path=%{dbpath} \
	--with-init-dir=/etc/rc.d/init.d \
	--with-initscript=sysv,systemd \
	--with-pipe-path=%{pipepath} \
	--with-pubconf-path=%{pubconfpath} \
	--with-python2-bindings%{!?with_python2:=no} \
	--with-python3-bindings%{!?with_python3:=no} \
	--with-systemdunitdir=%{systemdunitdir} \
	--with-test-dir=/dev/shm

%{__make}

%if %{with tests}
export CK_TIMEOUT_MULTIPLIER=10
%{__make} check
unset CK_TIMEOUT_MULTIPLIER
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	python3dir=%{py3_sitescriptdir}

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
#cp -p src/examples/rwtab $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/sssd

# Remove .la files created by libtool
%{__rm} \
	$RPM_BUILD_ROOT/%{_lib}/libnss_sss.la \
	$RPM_BUILD_ROOT/%{_lib}/libnfsidmap/sss.la \
	$RPM_BUILD_ROOT/%{_lib}/security/pam_sss.la \
	$RPM_BUILD_ROOT%{ldb_modulesdir}/memberof.la \
	$RPM_BUILD_ROOT%{_libdir}/cifs-utils/*.la \
	%{?with_krb5:$RPM_BUILD_ROOT%{_libdir}/krb5/plugins/libkrb5/sss*.la} \
	$RPM_BUILD_ROOT%{_libdir}/sssd/libsss_*.la \
	$RPM_BUILD_ROOT%{_libdir}/sssd/modules/lib*.la \
	$RPM_BUILD_ROOT%{_libdir}/lib*.la
%if %{with python2}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la
%py_postclean
%endif
%if %{with python3}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.la
%endif

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

%post	-n libsss_simpleifp -p /sbin/ldconfig
%postun	-n libsss_simpleifp -p /sbin/ldconfig

%files -f sssd.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sss_ssh_authorizedkeys
%attr(755,root,root) %{_bindir}/sss_ssh_knownhostsproxy
%attr(755,root,root) %{_sbindir}/sss_cache
%attr(755,root,root) %{_sbindir}/sssd
# sudo plugin
%attr(755,root,root) %{_libdir}/libsss_sudo.so
%dir %{_libdir}/sssd
# internal shared libraries
%attr(755,root,root) %{_libdir}/sssd/libsss_cert.so
%attr(755,root,root) %{_libdir}/sssd/libsss_child.so
%attr(755,root,root) %{_libdir}/sssd/libsss_config.so
%attr(755,root,root) %{_libdir}/sssd/libsss_crypt.so
%attr(755,root,root) %{_libdir}/sssd/libsss_debug.so
%attr(755,root,root) %{_libdir}/sssd/libsss_krb5_common.so
%attr(755,root,root) %{_libdir}/sssd/libsss_ldap_common.so
%attr(755,root,root) %{_libdir}/sssd/libsss_semanage.so
%attr(755,root,root) %{_libdir}/sssd/libsss_util.so
# modules
%attr(755,root,root) %{_libdir}/sssd/libsss_simple.so
%attr(755,root,root) %{_libdir}/sssd/libsss_ad.so
%attr(755,root,root) %{_libdir}/sssd/libsss_ipa.so
%attr(755,root,root) %{_libdir}/sssd/libsss_krb5.so
%attr(755,root,root) %{_libdir}/sssd/libsss_ldap.so
%attr(755,root,root) %{_libdir}/sssd/libsss_proxy.so
%dir %{_libdir}/sssd/modules
%attr(755,root,root) %{_libdir}/sssd/modules/libsss_autofs.so
%if "%{_libdir}" != "%{_libexecdir}"
%dir %{_libexecdir}/sssd
%endif
%attr(755,root,root) %{_libexecdir}/sssd/gpo_child
%attr(755,root,root) %{_libexecdir}/sssd/krb5_child
%attr(755,root,root) %{_libexecdir}/sssd/ldap_child
%attr(755,root,root) %{_libexecdir}/sssd/p11_child
%attr(755,root,root) %{_libexecdir}/sssd/proxy_child
%attr(755,root,root) %{_libexecdir}/sssd/selinux_child
%attr(755,root,root) %{_libexecdir}/sssd/sss_signal
%attr(755,root,root) %{_libexecdir}/sssd/sssd_autofs
%attr(755,root,root) %{_libexecdir}/sssd/sssd_be
%attr(755,root,root) %{_libexecdir}/sssd/sssd_ifp
%attr(755,root,root) %{_libexecdir}/sssd/sssd_nss
%if %{with krb5}
%attr(755,root,root) %{_libexecdir}/sssd/sssd_pac
%endif
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
%attr(755,root,root) /%{_lib}/libnfsidmap/sss.so
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
#%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rwtab.d/sssd
%attr(754,root,root) /etc/rc.d/init.d/sssd
%{systemdunitdir}/sssd.service
/etc/dbus-1/system.d/org.freedesktop.sssd.infopipe.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.sssd.infopipe.service
%{_mandir}/man1/sss_ssh_authorizedkeys.1*
%{_mandir}/man1/sss_ssh_knownhostsproxy.1*
%{_mandir}/man5/sss_rpcidmapd.5*
%{_mandir}/man5/sssd.conf.5*
%{_mandir}/man5/sssd-ad.5*
%{_mandir}/man5/sssd-ifp.5*
%{_mandir}/man5/sssd-ipa.5*
%{_mandir}/man5/sssd-krb5.5*
%{_mandir}/man5/sssd-ldap.5*
%{_mandir}/man5/sssd-simple.5*
%{_mandir}/man5/sssd-sudo.5*
%{_mandir}/man8/sss_cache.8*
%{_mandir}/man8/sssd.8*

%files client -f sssd_client.lang
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_sss.so.2
%attr(755,root,root) /%{_lib}/security/pam_sss.so
%attr(755,root,root) %{_libdir}/cifs-utils/cifs_idmap_sss.so
%if %{with krb5}
# XXX: verify locations
%attr(755,root,root) %{_libdir}/krb5/plugins/libkrb5/sssd_krb5_localauth_plugin.so
%attr(755,root,root) %{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%attr(755,root,root) %{_libdir}/krb5/plugins/libkrb5/sssd_pac_plugin.so
%endif
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
%attr(755,root,root) %{_sbindir}/sss_override
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
%{_mandir}/man8/sss_override.8*
%{_mandir}/man8/sss_seed.8*
%{_mandir}/man8/sss_useradd.8*
%{_mandir}/man8/sss_userdel.8*
%{_mandir}/man8/sss_usermod.8*

%if %{with python2}
%files -n python-sss
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pysss.so

%files -n python-sss-murmur
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pysss_murmur.so

%files -n python-sssdconfig
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/SSSDConfig
%{py_sitescriptdir}/SSSDConfig/*.py[co]
%{py_sitescriptdir}/SSSDConfig-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-sss
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/pysss.so

%files -n python3-sss-murmur
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/pysss_murmur.so

%files -n python3-sssdconfig
%defattr(644,root,root,755)
%dir %{py3_sitescriptdir}/SSSDConfig
%{py3_sitescriptdir}/SSSDConfig/*.py
%{py3_sitescriptdir}/SSSDConfig/__pycache__
%{py3_sitescriptdir}/SSSDConfig-%{version}-py*.egg-info
%endif

%files libwbclient
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/sssd/modules/libwbclient.so.*

%files libwbclient-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/sssd/modules/libwbclient.so
%{_includedir}/wbclient_sssd.h
%{_pkgconfigdir}/wbclient_sssd.pc

%files -n libipa_hbac
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipa_hbac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libipa_hbac.so.0

%files -n libipa_hbac-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipa_hbac.so
%{_includedir}/ipa_hbac.h
%{_pkgconfigdir}/ipa_hbac.pc

%if %{with python2}
%files -n python-libipa_hbac
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pyhbac.so
%endif

%if %{with python3}
%files -n python3-libipa_hbac
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/pyhbac.so
%endif

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

%if %{with python2}
%files -n python-libsss_nss_idmap
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/pysss_nss_idmap.so
%endif

%if %{with python3}
%files -n python3-libsss_nss_idmap
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/pysss_nss_idmap.so
%endif

%files -n libsss_simpleifp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsss_simpleifp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsss_simpleifp.so.0

%files -n libsss_simpleifp-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsss_simpleifp.so
%{_includedir}/sss_sifp.h
%{_includedir}/sss_sifp_dbus.h
%{_pkgconfigdir}/sss_simpleifp.pc
