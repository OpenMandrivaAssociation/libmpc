%define realname	mpc
%define libmajor	2
%define libname		%mklibname %{realname} %{libmajor}
%define libname_devel	%mklibname %{realname} -d

Summary:	Arithmetic of complex numbers with arbitrarily high precision and correct rounding
Name:		libmpc
Version:	0.9
Release:	%mkrel 2
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.multiprecision.org/%{realname}
Source0:	http://www.multiprecision.org/mpc/download/%{realname}-%{version}.tar.gz
BuildRequires:	libgmp-devel
BuildRequires:	libmpfr-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Patch0:		mpc-0.9-autoreconf.patch

%description
Mpc is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result. It is built upon and
follows the same principles as Mpfr. The library is written by Andreas Enge,
Philippe Théveny and Paul Zimmermann and is distributed under the Gnu Lesser
General Public License, either version 2.1 of the licence, or (at your option)
any later version. The Mpc library has been registered in France by the
Agence pour la Protection des Programmes on 2003-02-05 under the number
IDDN FR 001 060029 000 R P 2003 000 10000.

%package	-n %{libname}
Summary:	Arithmetic of complex numbers with arbitrarily high precision and correct rounding
Group:		System/Libraries

%description	-n %{libname}
Mpc is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result. It is built upon and
follows the same principles as Mpfr. The library is written by Andreas Enge,
Philippe Théveny and Paul Zimmermann and is distributed under the Gnu Lesser
General Public License, either version 2.1 of the licence, or (at your option)
any later version. The Mpc library has been registered in France by the
Agence pour la Protection des Programmes on 2003-02-05 under the number
IDDN FR 001 060029 000 R P 2003 000 10000.

%package	-n %{libname_devel}
Summary:	Development headers and libraries for MPC
Group:		Development/C
Requires(post):	info-install
Requires(preun):info-install
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description	-n %{libname_devel}
Development headers and libraries for MPC.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
autoreconf -ifs

%build
%configure2_5x			\
	--enable-shared		\
	--disable-static

%make

%install
%{__rm} -rf %{buildroot}
%makeinstall_std
mkdir -p %{buildroot}%{_docdir}/%{name}
install -m 0644 AUTHORS NEWS README TODO %{buildroot}%{_docdir}/%{name}

%check
make check

%clean
%{__rm} -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*
%{_libdir}/libmpc.so.%{libmajor}*

%files -n %{libname_devel}
%defattr(-,root,root)
%{_includedir}/mpc.h
%{_infodir}/mpc.info*
%{_libdir}/libmpc.la 
%{_libdir}/libmpc.so
