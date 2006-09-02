#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_without	smp		# without smp version
#

%define		_orig_name	eplip
%define		_rel	2

Summary:	EPLIP driver for 2.6.x kernels
Summary(pl):	Sterownik EPLIP dla j±der 2.6.x
Name:		kernel-net-eplip
Version:	0.5.6
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://e-plip.sourceforge.net/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	43019250e7227857ae13bdd39a45494d
Patch0:		%{name}-1.patch
Patch1:		kernel-eplip-WIRING.patch
Patch2:		%{name}-2.patch
Patch3:		%{name}-module_param_array.patch
URL:		http://e-plip.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-module-build}
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	modutils
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
EPLIP (Enhanced Parallel Line IP) driver module for 2.6.x kernels.

%description -l pl
Modu³ sterownika EPLIP (Enhanced Parallel Line IP) dla j±der 2.6.x.

%package -n kernel-smp-net-eplip
Summary:	EPLIP driver for 2.6.x SMP kernels
Summary(pl):	Sterownik EPLIP dla j±der 2.6.x SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	modutils

%description -n kernel-smp-net-eplip
EPLIP (Enhanced Parallel Line IP) driver module for 2.6.x SMP kernels.

%description -n kernel-smp-net-eplip -l pl
Modu³ sterownika EPLIP (Enhanced Parallel Line IP) dla j±der 2.6.x
SMP.

%prep
%setup -q -n %{_orig_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
install -d build-done/{UP,SMP}
rm -rf include
install -d o/include/{linux,config}
ln -sf %{_kernelsrcdir}/config-up o/.config
ln -sf %{_kernelsrcdir}/include/linux/autoconf-up.h o/include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} o/include/asm
ln -sf %{_kernelsrcdir}/Module.symvers-up o/Module.symvers
#touch include/config/MARKER
cat <<EOF > Makefile
CONFIG_X86=1
CONFIG_ISA=1
obj-m += eplip.o
eplip-objs := eplip-drv.o
EOF
%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%{__make} -C %{_kernelsrcdir} modules \
	SYSRC=%{_kernelsrcdir} \
	SYSOUT=$PWD/o \
	M=$PWD \
	O=$PWD/o \
	V=1
mv *.ko build-done/UP

%if %{with smp}
ln -sf %{_kernelsrcdir}/config-smp .config
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf-smp.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm
ln -sf %{_kernelsrcdir}/Module.symvers-smp Module.symvers
#touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} O=$PWD prepare scripts
%{__make} -C %{_kernelsrcdir} clean \
	RCS_FIND_IGNORE="-name '*.ko' -o" \
	SYSSRC=%{_kernelsrcdir} \
	SYSOUT=$PWD/o \
	M=$PWD O=$PWD/o \
	V=1
%{__make} -C %{_kernelsrcdir} modules \
	SYSRC=%{_kernelsrcdir} \
	SYSOUT=$PWD \
	M=$PWD \
	O=$PWD \
	V=1

mv *.ko build-done/SMP
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net
cp build-done/UP/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net

%if %{with smp}
cp build-done/SMP/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-eplip
%depmod %{_kernel_ver}

%postun	-n kernel-net-eplip
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-eplip
%depmod %{_kernel_ver}

%postun	-n kernel-smp-net-eplip
%depmod %{_kernel_ver}

%files -n kernel-net-eplip
%defattr(644,root,root,755)
%doc ChangeLog LAME-TESTS README TODO TODO-done WIRING
/lib/modules/%{_kernel_ver}/kernel/drivers/net/*

%if %{with smp}
%files -n kernel-smp-net-eplip
%defattr(644,root,root,755)
%doc ChangeLog LAME-TESTS README TODO TODO-done WIRING
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/*
%endif
