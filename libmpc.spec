%define oname mpc
%define major 3
%define libname %mklibname %{oname} %{major}
%define devname %mklibname %{oname} -d

%bcond_with	uclibc

Summary:	Complex numbers arithmetic with arbitrarily high precision and correct rounding
Name:		libmpc
Version:	1.0.3
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.multiprecision.org/%{oname}
Source0:	http://www.multiprecision.org/mpc/download/%{oname}-%{version}.tar.gz
BuildRequires:	gmp-devel
BuildRequires:	mpfr-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel
BuildRequires:	uclibc-gmp-devel
BuildRequires:	uclibc-mpfr-devel
%endif

%description
Mpc is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result. It is built upon and
follows the same principles as Mpfr. The library is written by Andreas Enge,
Philippe Théveny and Paul Zimmermann and is distributed under the Gnu Lesser
General Public License, either version 2.1 of the licence, or (at your option)
any later version. The Mpc library has been registered in France by the
Agence pour la Protection des Programmes on 2003-02-05 under the number
IDDN FR 001 060029 000 R P 2003 000 10000.

%package -n	%{libname}
Summary:	Complex numbers arithmetic with arbitrarily high precision and correct rounding
Group:		System/Libraries

%description -n	%{libname}
Mpc is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result. It is built upon and
follows the same principles as Mpfr. The library is written by Andreas Enge,
Philippe Théveny and Paul Zimmermann and is distributed under the Gnu Lesser
General Public License, either version 2.1 of the licence, or (at your option)
any later version. The Mpc library has been registered in France by the
Agence pour la Protection des Programmes on 2003-02-05 under the number
IDDN FR 001 060029 000 R P 2003 000 10000.

%if %{with uclibc}
%package -n	uclibc-%{libname}
Summary:	uClibc build of libmpc
Group:		System/Libraries

%description -n	uclibc-%{libname}
Mpc is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result. It is built upon and
follows the same principles as Mpfr. The library is written by Andreas Enge,
Philippe Théveny and Paul Zimmermann and is distributed under the Gnu Lesser
General Public License, either version 2.1 of the licence, or (at your option)
any later version. The Mpc library has been registered in France by the
Agence pour la Protection des Programmes on 2003-02-05 under the number
IDDN FR 001 060029 000 R P 2003 000 10000.

%package -n	uclibc-%{devname}
Summary:	Development headers and libraries for MPC
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	uclibc-%{libname} = %{EVRD}
Provides:	uclibc-%{name}-devel = %{EVRD}
Conflicts:	%{devname} < 1.0.2-7

%description -n	uclibc-%{devname}
Development headers and libraries for MPC.
%endif

%package -n	%{devname}
Summary:	Development headers and libraries for MPC
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
Development headers and libraries for MPC.

%prep
%setup -qn %{oname}-%{version}

%build
CONFIGURE_TOP=$PWD
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--enable-shared
%make
popd
%endif

mkdir -p glibc
pushd glibc
%configure \
	--enable-shared
%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
%endif
%makeinstall_std -C glibc

%check
make -C glibc check

%files -n %{libname}
%{_libdir}/libmpc.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libmpc.so.%{major}*

%files -n uclibc-%{devname}
%{uclibc_root}%{_libdir}/libmpc.so
%endif

%files -n %{devname}
%doc AUTHORS NEWS README TODO
%{_includedir}/mpc.h
%{_infodir}/mpc.info*
%{_libdir}/libmpc.so
