# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global build_api_doc 1

Name:           python-nss
Version:        0.11
Release:        3%{?dist}
Summary:        Python bindings for Network Security Services (NSS)

Group:          Development/Languages
License:        MPLv1.1 or GPLv2+ or LGPLv2+
URL:            ftp://ftp.mozilla.org/pub/mozilla.org/security/python-nss
Source0:        ftp://ftp.mozilla.org/pub/mozilla.org/security/python-nss/releases/PYNSS_RELEASE_0_11_0/src/python-nss-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: python-nss-0.11-family.patch

%global docdir %{_docdir}/%{name}-%{version}

# We don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

BuildRequires: python-devel
BuildRequires: python-setuptools-devel
BuildRequires: python-docutils
BuildRequires: nspr-devel
BuildRequires: nss-devel
BuildRequires: epydoc

%description
This package provides Python bindings for Network Security Services
(NSS) and the Netscape Portable Runtime (NSPR).

NSS is a set of libraries supporting security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3
certificates, and other security standards. Specific NSS
implementations have been FIPS-140 certified.

%package doc
Group: Documentation
Summary: API documentation and examples
Requires: %{name} = %{version}-%{release}

%description doc
API documentation and examples

%prep
%setup -q
%patch1 -p0 -b.family

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %{__python} setup.py build
%if %build_api_doc
%{__python} setup.py build_doc
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install  -O1 --install-platlib %{python_sitearch} --skip-build --root $RPM_BUILD_ROOT
%{__python} setup.py install_doc --docdir %{docdir} --skip-build --root $RPM_BUILD_ROOT

# Remove execution permission from any example/test files in docdir
find $RPM_BUILD_ROOT/%{docdir} -type f | xargs chmod a-x

# Set correct permissions on .so files
chmod 0755 $RPM_BUILD_ROOT/%{python_sitearch}/nss/*.so


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitearch}/*
%doc %{docdir}/ChangeLog
%doc %{docdir}/LICENSE.gpl
%doc %{docdir}/LICENSE.lgpl
%doc %{docdir}/LICENSE.mpl
%doc %{docdir}/README

%files doc
%defattr(-,root,root,-)
%doc %{docdir}/examples
%doc %{docdir}/test
%if %build_api_doc
%doc %{docdir}/api
%endif

%changelog
* Tue Mar 22 2011 John Dennis <jdennis@redhat.com> - 0.11-3
- Resolves: #689807
  Add family parameter to Socket constructors in examples and doc.
  Mark implicit family parameter as deprecated.
  Raise exception if Socket family does not match NetworkAddress family.
  Add --server-subject to setup_certs.py (made testing IPv6 easier without DNS)

* Tue Mar  1 2011 John Dennis <jdennis@redhat.com> - 0.11-2
- Resolves: #670951
- Resolves: #674014
  Rebuild enabling api doc generation, it had been disabled because
  the buildroots on 6.1 contained a verion of epydoc that crashed,
  release engineering has updated epydoc in the buildroots.
  There are NO changes in the package source.

* Wed Feb 23 2011 John Dennis <jdennis@redhat.com> - 0.11-1
- Resolves: #670951
- Resolves: #674014

  * Better support for IPv6

  * Add AddrInfo class to support IPv6 address resolution. Supports
    iteration over it's set of NetworkAddress objects and provides
    hostname, canonical_name object properties.

  * Add PR_AI_* constants.

  * NetworkAddress constructor and NetworkAddress.set_from_string() added
    optional family parameter. This is necessary for utilizing
    PR_GetAddrInfoByName().

  * NetworkAddress initialized via a string paramter are now initalized via
    PR_GetAddrInfoByName using family.

  * Add NetworkAddress.address property to return the address sans the
    port as a string. NetworkAddress.str() includes the port. For IPv6 the
    a hex string must be enclosed in brackets if a port is appended to it,
    the bracketed hex address with appended with a port is unappropriate
    in some circumstances, hence the new address property to permit either
    the address string with a port or without a port.

  * Fix the implementation of the NetworkAddress.family property, it was
    returning bogus data due to wrong native data size.

  * HostEntry objects now support iteration and indexing of their
    NetworkAddress members.

  * Add io.addr_family_name() function to return string representation of
    PR_AF_* constants.

  * Modify example and test code to utilize AddrInfo instead of deprecated
    NetworkAddress functionality. Add address family command argument to
    ssl_example.

  * Fix pty import statement in test/setup_certs.py

    Deprecated Functionality:
    -------------------------

  * NetworkAddress initialized via a string paramter is now
    deprecated. AddrInfo should be used instead.

  * NetworkAddress.set_from_string is now deprecated. AddrInfo should be
    used instead.

  * NetworkAddress.hostentry is deprecated. It was a bad idea,
    NetworkAddress objects can support both IPv4 and IPv6, but a HostEntry
    object can only support IPv4. Plus the implementation depdended on
    being able to perform a reverse DNS lookup which is not always
    possible.

  * HostEntry.get_network_addresses() and HostEntry.get_network_address()
    are now deprecated. In addition their port parameter is now no longer
    respected. HostEntry objects now support iteration and
    indexing of their NetworkAddress and that should be used to access
    their NetworkAddress objects instead.

* Tue Jan 11 2011 John Dennis <jdennis@redhat.com> - 0.10-3
- Related: #619743
- Fix all rpmlint warnings
- doc for license, changelog etc. now in main package,
  doc subpackage now only contains api doc, examples, test, etc.
- Filter provides for .so files
- Remove execute permission on everything in docdir
- Capitalize description

* Tue Jan 11 2011 John Dennis <jdennis@redhat.com> - 0.10-2
- Related: #619743
- split documentation out into separate doc sub-package
  and make building api documentation optional

* Mon Jan 10 2011 John Dennis <jdennis@redhat.com> - 0.10-1
- Resolves: #619743, Update to latest upstream, changes include:
- The following classes were added:
    InitParameters
    InitContext

-The following module functions were added:
    nss.nss.nss_initialize()
    nss.nss.nss_init_context()
    nss.nss.nss_shutdown_context()
    nss.nss.nss_init_flags()

- add nss_is_initialized()

- Remove nss_init_nodb() when nss modules loads from previous version
  apparently this prevents subsequent calls to nss_init with a
  database to silently fail.
- Clean up some cruft in doc/examples/verify_server.py

- Invoke nss_init_nodb() when nss modules loads, this prevents segfaults
  in NSS if Python programmer forgot to call one of the NSS
  initialization routines.

- Rename the classes X500Name, X500RDN, X500AVA to DN, RDN, AVA
  respectively.

- DN and RDN objects now return a list of their contents when indexed by
  type, this is to support multi-valued items.

- Fix bug where AVA object's string representation did not include it's
  type.

- Enhance test/test_cert_components.py unit test to test for above
  changes.

- Add CertificateRequest object

- Fix incomplete read bug (due to read ahead buffer bookkeeping).
- Remove python-nss specific httplib.py, no longer needed
  python-nss now compatible with standard library
- Rewrite httplib_example.py to use standard library and illustrate
  ssl, non-ssl, connection class, http class usage

- add nss.cert_usage_flags(), use it in ssl_example.py

- Add format_lines() & format() methods to the new certificate extension objects.
- Add printing of certificate extensions.
- Add BasicContstraints certificate extension.
- Fix several reference counting and memory problems discovered with valgrind.

- fold in more ref counting patches from Miloslav Trmač <mitr@redhat.com>
  into upstream.
  Did not bump upstream version, just bumped release ver in this spec file.

- Unicode objects now accepted as well as str objects for
  interfaces expecting a string.

- Sockets were enhanced thusly:
    - Threads will now yield during blocking IO.
    - Socket.makefile() reimplemented
          file object methods that had been missing (readlines(), sendall(),
          and iteration) were implemented, makefile now just returns the same
          Socket object but increments an "open" ref count. Thus a Socket
          object behaves like a file object and must be closed once for each
          makefile() call before it's actually closed.
    - Sockets now support the iter protocol
    - Add Socket.readlines(), Socket.sendall()

- The following classes were added:
    AuthKeyID
    BasicConstraints
    CRLDistributionPoint
    CRLDistributionPts
    CertificateExtension
    GeneralName
    SignedCRL
    X500AVA
    X500Name
    X500RDN

- The following module functions were added:
    nss.nss.cert_crl_reason_from_name()
    nss.nss.cert_crl_reason_name()
    nss.nss.cert_general_name_type_from_name()
    nss.nss.cert_general_name_type_name()
    nss.nss.cert_usage_flags()
    nss.nss.decode_der_crl()
    nss.nss.der_universal_secitem_fmt_lines()
    nss.nss.import_crl()
    nss.nss.make_line_pairs()
    nss.nss.oid_dotted_decimal()
    nss.nss.oid_str()
    nss.nss.oid_tag()
    nss.nss.oid_tag_name()
    nss.nss.read_der_from_file()
    nss.nss.x509_alt_name()
    nss.nss.x509_ext_key_usage()
    nss.nss.x509_key_usage()

- The following class methods and properties were added:
  Note: it's a method if the name is suffixed with (), a propety otherwise
    Socket.next()
    Socket.readlines()
    Socket.sendall()
    SSLSocket.next()
    SSLSocket.readlines()
    SSLSocket.sendall()
    AuthKeyID.key_id
    AuthKeyID.serial_number
    AuthKeyID.get_general_names()
    CRLDistributionPoint.issuer
    CRLDistributionPoint.get_general_names()
    CRLDistributionPoint.get_reasons()
    CertDB.find_crl_by_cert()
    CertDB.find_crl_by_name()
    Certificate.extensions
    CertificateExtension.critical
    CertificateExtension.name
    CertificateExtension.oid
    CertificateExtension.oid_tag
    CertificateExtension.value
    GeneralName.type_enum
    GeneralName.type_name
    GeneralName.type_string
    SecItem.der_to_hex()
    SecItem.get_oid_sequence()
    SecItem.to_hex()
    SignedCRL.delete_permanently()
    X500AVA.oid
    X500AVA.oid_tag
    X500AVA.value
    X500AVA.value_str
    X500Name.cert_uid
    X500Name.common_name
    X500Name.country_name
    X500Name.dc_name
    X500Name.email_address
    X500Name.locality_name
    X500Name.org_name
    X500Name.org_unit_name
    X500Name.state_name
    X500Name.add_rdn()
    X500Name.has_key()
    X500RDN.has_key()

- The following module functions were removed:
  Note: use nss.nss.oid_tag() instead
    nss.nss.sec_oid_tag_from_name()
    nss.nss.sec_oid_tag_name()
    nss.nss.sec_oid_tag_str()

- The following files were added:
    doc/examples/cert_dump.py
    test/test_cert_components.py

- Apply patches from  Miloslav Trmač <mitr@redhat.com>
  for ref counting and threading support. Thanks Miloslav!

- Review all ref counting, numerous ref counting fixes

- Implement cyclic garbage collection support by
  adding object traversal and clear methods

- Identify static variables, move to thread local storage

* Tue Apr  6 2010 John Dennis <jdennis@redhat.com> - 0.8-3
- fix URL tag in spec file per package wrangler review request
  Related: rhbz#543948

* Wed Mar 24 2010 John Dennis <jdennis@redhat.com> - 0.8-2
- change %%define to %%global per spec file review request
  Related: rhbz#543948

* Mon Sep 21 2009 John Dennis <jdennis@redhat.com> - 0.8-1
- The following methods, properties  and functions were added:
  SecItem.type SecItem.len, SecItem.data
  PK11SymKey.key_data, PK11SymKey.key_length, PK11SymKey.slot
  create_context_by_sym_key
  param_from_iv
  generate_new_param
  get_iv_length
  get_block_size
  get_pad_mechanism
- SecItem's now support indexing and slicing on their data
- Clean up parsing and parameter validation of variable arg functions

* Fri Sep 18 2009 John Dennis <jdennis@redhat.com> - 0.7-1
- add support for symmetric encryption/decryption
  more support for digests (hashes)

  The following classes were added:
  PK11SymKey PK11Context

  The following methods and functions were added:
  get_best_wrap_mechanism          get_best_key_length
  key_gen                          derive
  get_key_length                   digest_key
  clone_context                    digest_begin
  digest_op                        cipher_op
  finalize                         digest_final
  read_hex                         hash_buf
  sec_oid_tag_str                  sec_oid_tag_name
  sec_oid_tag_from_name            key_mechanism_type_name
  key_mechanism_type_from_name     pk11_attribute_type_name
  pk11_attribute_type_from_name    get_best_slot
  get_internal_key_slot            create_context_by_sym_key
  import_sym_key                   create_digest_context
  param_from_iv                    param_from_algid
  generate_new_param               algtag_to_mechanism
  mechanism_to_algtag

  The following files were added:
  cipher_test.py digest_test.py

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 John Dennis <jdennis@redhat.com> - 0.6-2
- restore nss.nssinit(), make deprecated

* Wed Jul  8 2009 John Dennis <jdennis@redhat.com> - 0.6-1
- fix bug #510343 client_auth_data_callback seg faults if False
  is returned from callback

* Wed Jul  1 2009 John Dennis <jdennis@redhat.com> - 0.5-1
- restore ssl.nss_init and ssl.nss_shutdown but make them deprecated
  add __version__ string to nss module

* Tue Jun 30 2009 John Dennis <jdennis@redhat.com> - 0.4-1
- add binding for NSS_NoDB_Init(), bug #509002
  move nss_init and nss_shutdown from ssl module to nss module

* Thu Jun  4 2009 John Dennis <jdennis@redhat.com> - 0.3-1
- installed source code in Mozilla CVS repository
  update URL tag to point to CVS repositoy
  (not yet a valid URL, still have to coordinate with Mozilla)
  minor tweak to src directory layout

* Mon Jun  1 2009 John Dennis <jdennis@redhat.com> - 0.2-1
- Convert licensing to MPL tri-license
- apply patch from bug #472805, (Miloslav Trmač)
  Don't allow closing a socket twice, that causes crashes.
  New function nss.io.Socket.new_socket_pair()
  New function nss.io.Socket.poll()
  New function nss.io.Socket.import_tcp_socket()
  New method nss.nss.Certificate.get_subject_common_name()
  New function nss.nss.generate_random()
  Fix return value creation in SSLSocket.get_security_status
  New function nss.ssl.SSLSocket.import_tcp_socket()

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1-2
- Rebuild for Python 2.6

* Tue Sep  9 2008 John Dennis <jdennis@redhat.com> - 0.1-1
- clean up ssl_example.py, fix arg list in get_cert_nicknames,
   make certdir cmd line arg consistent with other NSS tools
- update httplib.py to support client auth, add httplib_example.py which illustrates it's use
- fix some documentation
- fix some type usage which were unsafe on 64-bit

* Wed Jul  9 2008 John Dennis <jdennis@redhat.com> - 0.0-2
- add docutils to build requires so restructured text works

* Fri Jun 27 2008 John Dennis <jdennis@redhat.com> - 0.0-1
- initial release


