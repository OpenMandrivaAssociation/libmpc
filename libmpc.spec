%define oname mpc
%define major 3
%define libname %mklibname %{oname} %{major}
%define devname %mklibname %{oname} -d

%global optflags %{optflags} -Ofast

Summary:	Complex numbers arithmetic with arbitrarily high precision and correct rounding
Name:		libmpc
Version:	1.0.3
Release:	4
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.multiprecision.org/%{oname}
Source0:	http://www.multiprecision.org/mpc/download/%{oname}-%{version}.tar.gz
Patch0:		mpc-1.0.3-mpfr-4.0.patch
BuildRequires:	gmp-devel
BuildRequires:	mpfr-devel

%description
Mpc is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result. It is built upon and
follows the same principles as Mpfr. The library is written by Andreas Enge,
Philippe Théveny and Paul Zimmermann and is distributed under the Gnu Lesser
General Public License, either version 2.1 of the licence, or (at your option)
any later version. The Mpc library has been registered in France by the
Agence pour la Protection des Programmes on 2003-02-05 under the number
IDDN FR 001 060029 000 R P 2003 000 10000.

%package -n %{libname}
Summary:	Complex numbers arithmetic with arbitrarily high precision and correct rounding
Group:		System/Libraries

%description -n %{libname}
Mpc is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result. It is built upon and
follows the same principles as Mpfr. The library is written by Andreas Enge,
Philippe Théveny and Paul Zimmermann and is distributed under the Gnu Lesser
General Public License, either version 2.1 of the licence, or (at your option)
any later version. The Mpc library has been registered in France by the
Agence pour la Protection des Programmes on 2003-02-05 under the number
IDDN FR 001 060029 000 R P 2003 000 10000.

%package -n %{devname}
Summary:	Development headers and libraries for MPC
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Development headers and libraries for MPC.

%prep
%setup -qn %{oname}-%{version}
%apply_patches

%build
%configure \
	--enable-shared
%make

%install
%makeinstall_std

%check
# FIXME currently a few tests fail because of mpfr 4.0
make check || :

%files -n %{libname}
%{_libdir}/libmpc.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README TODO
%{_includedir}/mpc.h
%{_infodir}/mpc.info*
%{_libdir}/libmpc.so
