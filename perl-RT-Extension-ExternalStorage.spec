# TODO:
# - get rid of BR rt requirement
#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	RT
%define		pnam	Extension-ExternalStorage
Summary:	RT::Extension::ExternalStorage - Store attachments outside the database
Name:		perl-RT-Extension-ExternalStorage
Version:	0.60
Release:	2
License:	GPL
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/RT/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	5a4bbde7b2aef2115da38ef682312ed3
URL:		http://search.cpan.org/dist/RT-Extension-ExternalStorage/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rt
%if %{with tests}
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
By default, RT stores attachments in the database. This extension
moves all attachments that RT does not need efficient access to (which
include textual content and images) to outside of the database. This
may either be on local disk, or to a cloud storage solution. This
decreases the size of RT's database, in turn decreasing the burden of
backing up RT's database, at the cost of adding additional locations
which must be configured or backed up.

The files are initially stored in the database when RT receives them;
this guarantees that the user does not need to wait for the file to be
transferred to disk or to the cloud, and makes it durable to transient
failures of cloud connectivity. The provided bin/extract-attachments
script, to be run regularly via cron, takes care of moving attachments
out of the database at a later time.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%dir %{perl_vendorlib}/RT/Extension
%{perl_vendorlib}/RT/Extension/*.pm
%{perl_vendorlib}/RT/Extension/ExternalStorage
%{_mandir}/man3/*
