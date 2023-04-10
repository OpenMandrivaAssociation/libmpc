%define oname mpc
%define major 3
%define libname %mklibname %{oname} %{major}
%define devname %mklibname %{oname} -d

%global optflags %{optflags} -O3

# (tpg) enable PGO build
%if ! %{cross_compiling}
%bcond_without pgo
%endif

Summary:	Complex numbers arithmetic with arbitrarily high precision and correct rounding
Name:		libmpc
Version:	1.3.1
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.multiprecision.org/%{oname}
Source0:	https://ftp.gnu.org/gnu/mpc/mpc-%{version}.tar.gz
Patch0:		mpc-1.3.0-bench-compile.patch
BuildRequires:	pkgconfig(gmp)
BuildRequires:	pkgconfig(mpfr)
BuildRequires:	texinfo

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
%autosetup -n %{oname}-%{version} -p1

libtoolize
aclocal -I m4
autoheader
automake -a
autoconf

%build
%if %{with pgo}
export LD_LIBRARY_PATH="$(pwd)"

CFLAGS="%{optflags} -fprofile-generate -mllvm -vp-counters-per-site=32" \
CXXFLAGS="%{optflags} -fprofile-generate" \
LDFLAGS="%{build_ldflags} -fprofile-generate" \
%configure \
	--enable-shared

%make_build
make check || :
cd tools/bench
make bench
cd -
unset LD_LIBRARY_PATH
llvm-profdata merge --output=%{name}-llvm.profdata $(find . -name "*.profraw" -type f)
PROFDATA="$(realpath %{name}-llvm.profdata)"
rm -f *.profraw
make clean

CFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
CXXFLAGS="%{optflags} -fprofile-use=$PROFDATA" \
LDFLAGS="%{build_ldflags} -fprofile-use=$PROFDATA" \
%endif
%configure \
	--enable-shared

%make_build

%install
%make_install

%if ! %{cross_compiling}
%ifnarch aarch64
%check
make check
%endif
%endif

%files -n %{libname}
%{_libdir}/libmpc.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README TODO
%{_includedir}/mpc.h
%doc %{_infodir}/mpc.info*
%{_libdir}/libmpc.so
