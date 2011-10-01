# TODO
#error: Failed build dependencies:
#        keyutils-libs-devel is needed by sssd-1.6.1-0.1.src
#        krb5-devel >= 1.9 is needed by sssd-1.6.1-0.1.src
#        libcollection-devel is needed by sssd-1.6.1-0.1.src
#        libdhash-devel >= 0.4.2 is needed by sssd-1.6.1-0.1.src
#        libini_config-devel is needed by sssd-1.6.1-0.1.src
#        libldb-devel = 1.1.0 is needed by sssd-1.6.1-0.1.src
#        libtdb-devel is needed by sssd-1.6.1-0.1.src
#        libtevent-devel is needed by sssd-1.6.1-0.1.src

%define		ldb_version 1.1.0
Summary:	System Security Services Daemon
Name:		sssd
Version:	1.6.1
Release:	0.1
License:	GPL v3+
Group:		Applications/System
URL:		http://fedorahosted.org/sssd/
Source0:	https://fedorahosted.org/released/sssd/%{name}-%{version}.tar.gz
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bind-utils
BuildRequires:	c-ares-devel
BuildRequires:	check-devel
BuildRequires:	dbus-devel
BuildRequires:	dbus-libs
BuildRequires:	docbook-style-xsl
BuildRequires:	doxygen
BuildRequires:	gettext-devel
BuildRequires:	keyutils-libs-devel
BuildRequires:	krb5-devel >= 1.9
BuildRequires:	libcollection-devel
BuildRequires:	libdhash-devel >= 0.4.2
BuildRequires:	libini_config-devel
BuildRequires:	libldb-devel = %{ldb_version}
BuildRequires:	libnl-devel
BuildRequires:	libselinux-devel
BuildRequires:	libsemanage-devel
BuildRequires:	libtalloc-devel
BuildRequires:	libtdb-devel
BuildRequires:	libtevent-devel
BuildRequires:	libtool
BuildRequires:	libunistring-devel
BuildRequires:	libxml2
BuildRequires:	libxslt
BuildRequires:	m4
BuildRequires:	nscd
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel
BuildRequires:	popt-devel
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	/sbin/ldconfig
Requires:	cyrus-sasl-gssapi
Requires:	krb5-libs >= 1.9
Requires:	libldb = %{ldb_version}
Requires:	libtdb >= 1.1.3
Requires:	%{name}-client = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		servicename		sssd
%define		sssdstatedir	%{_localstatedir}/lib/sss
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

%package client
Summary:	SSSD Client libraries for NSS and PAM
License:	LGPLv3+
Group:		Applications/System

%description client
Provides the libraries needed by the PAM and NSS stacks to connect to
the SSSD service.

%package tools
Summary:	Userspace tools for use with the SSSD
License:	GPL v3+
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description tools
Provides userspace tools for manipulating users, groups, and nested
groups in SSSD when using id_provider = local in /etc/sssd/sssd.conf.

Also provides a userspace tool for generating an obfuscated LDAP
password for use with ldap_default_authtok_type = obfuscated_password.

%package -n libipa_hbac
Summary:	FreeIPA HBAC Evaluator library
License:	LGPLv3+
Group:		Development/Libraries

%description -n libipa_hbac
Utility library to validate FreeIPA HBAC rules for authorization
requests

%package -n libipa_hbac-devel
Summary:	FreeIPA HBAC Evaluator library
License:	LGPLv3+
Group:		Development/Libraries
Requires:	libipa_hbac = %{version}-%{release}

%description -n libipa_hbac-devel
Utility library to validate FreeIPA HBAC rules for authorization
requests

%package -n python-libipa_hbac
Summary:	Python bindings for the FreeIPA HBAC Evaluator library
License:	LGPLv3+
Group:		Development/Libraries
Requires:	libipa_hbac = %{version}-%{release}
Obsoletes:	libipa_hbac-python

%description -n python-libipa_hbac
This package contains the bindings so that libipa_hbac can be used by
Python applications.

%prep
%setup -q

%build
autoreconf -ivf
%configure \
	--with-db-path=%{dbpath} \
	--with-pipe-path=%{pipepath} \
	--with-pubconf-path=%{pubconfpath} \
	--with-init-dir=%{_initrddir} \
	--enable-nsslibdir=/%{_lib} \
	--enable-pammoddir=/%{_lib}/security \
	--disable-static \
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
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sssd
cp -p src/examples/sssd.conf $RPM_BUILD_ROOT%{_sysconfdir}/sssd/sssd.conf
cp -p src/config%{_sysconfdir}/sssd.api.conf $RPM_BUILD_ROOT%{_sysconfdir}/sssd/sssd.api.conf
cp -p src/config%{_sysconfdir}/sssd.api.d/* $RPM_BUILD_ROOT%{_sysconfdir}/sssd/sssd.api.d/

# Copy default logrotate file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
cp -p src/examples/logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sssd

# Make sure SSSD is able to run on read-only root
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/rwtab.d
cp -p src/examples/rwtab $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/sssd

# Remove .la files created by libtool
%{__rm} \
    $RPM_BUILD_ROOT/%{_lib}/libnss_sss.la \
    $RPM_BUILD_ROOT/%{_lib}/security/pam_sss.la \
    $RPM_BUILD_ROOT/%{ldb_modulesdir}/memberof.la \
    $RPM_BUILD_ROOT/%{_libdir}/sssd/libsss_ldap.la \
    $RPM_BUILD_ROOT/%{_libdir}/sssd/libsss_proxy.la \
    $RPM_BUILD_ROOT/%{_libdir}/sssd/libsss_krb5.la \
    $RPM_BUILD_ROOT/%{_libdir}/sssd/libsss_ipa.la \
    $RPM_BUILD_ROOT/%{_libdir}/sssd/libsss_simple.la \
    $RPM_BUILD_ROOT/%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.la \
    $RPM_BUILD_ROOT/%{_libdir}/libipa_hbac.la \
    $RPM_BUILD_ROOT/%{py_sitedir}/pysss.la \
    $RPM_BUILD_ROOT/%{py_sitedir}/pyhbac.la

touch sssd_tools.lang
for man in `find $RPM_BUILD_ROOT/%{_mandir}/??/man?/ -type f | sed -e "s#$RPM_BUILD_ROOT/%{_mandir}/##"`; do
	lang=`echo $man | cut -c 1-2`
	case `basename $man` in
		sss_*)
			echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_tools.lang
		;;
		*)
			echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
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

%post	client -p /sbin/ldconfig
%postun	client -p /sbin/ldconfig

%post	-n libipa_hbac -p /sbin/ldconfig
%postun	-n libipa_hbac -p /sbin/ldconfig

%files -f sssd.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/sssd
%{_libexecdir}/%{servicename}
%{_libdir}/%{name}/
%attr(755,root,root) %{ldb_modulesdir}/memberof.so
%dir %{sssdstatedir}
%attr(700,root,root) %dir %{dbpath}
%dir %{pipepath}
%dir %{pubconfpath}
%attr(700,root,root) %dir %{pipepath}/private
%attr(750,root,root) %dir %{_var}/log/%{name}
%attr(700,root,root) %dir %{_sysconfdir}/sssd
%config(noreplace) %{_sysconfdir}/sssd/sssd.conf
%config(noreplace) /etc/logrotate.d/sssd
%config(noreplace) %{_sysconfdir}/rwtab.d/sssd
%config %{_sysconfdir}/sssd/sssd.api.conf
%attr(700,root,root) %dir %{_sysconfdir}/sssd/sssd.api.d
%config %{_sysconfdir}/sssd/sssd.api.d/
%{_mandir}/man5/sssd.conf.5*
%{_mandir}/man5/sssd-ipa.5*
%{_mandir}/man5/sssd-krb5.5*
%{_mandir}/man5/sssd-ldap.5*
%{_mandir}/man5/sssd-simple.5*
%{_mandir}/man8/sssd.8*
%attr(755,root,root) %{py_sitedir}/pysss.so
%{py_sitescriptdir}/*.py[co]

%files client -f sssd_tools.lang
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libnss_sss.so.2
%attr(755,root,root) /%{_lib}/security/pam_sss.so
%attr(755,root,root) %{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%{_mandir}/man8/pam_sss.8*
%{_mandir}/man8/sssd_krb5_locator_plugin.8*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/sss_useradd
%attr(755,root,root) %{_sbindir}/sss_userdel
%attr(755,root,root) %{_sbindir}/sss_usermod
%attr(755,root,root) %{_sbindir}/sss_groupadd
%attr(755,root,root) %{_sbindir}/sss_groupdel
%attr(755,root,root) %{_sbindir}/sss_groupmod
%attr(755,root,root) %{_sbindir}/sss_groupshow
%attr(755,root,root) %{_sbindir}/sss_obfuscate
%attr(755,root,root) %{_sbindir}/sss_cache
%{_mandir}/man8/sss_groupadd.8*
%{_mandir}/man8/sss_groupdel.8*
%{_mandir}/man8/sss_groupmod.8*
%{_mandir}/man8/sss_groupshow.8*
%{_mandir}/man8/sss_useradd.8*
%{_mandir}/man8/sss_userdel.8*
%{_mandir}/man8/sss_usermod.8*
%{_mandir}/man8/sss_obfuscate.8*
%{_mandir}/man8/sss_cache.8*

%files -n libipa_hbac
%defattr(644,root,root,755)
%{_libdir}/libipa_hbac.so.*

%files -n libipa_hbac-devel
%defattr(644,root,root,755)
%{_includedir}/ipa_hbac.h
%{_libdir}/libipa_hbac.so
%{_pkgconfigdir}/ipa_hbac.pc

%files -n python-libipa_hbac
%defattr(644,root,root,755)
%{py_sitedir}/pyhbac.so
%{py_sitescriptdir}/*.egg-info
