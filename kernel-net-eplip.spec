# $Revision: 1.1 $
#
# TODO: UP/SMP (if this spec is useful for something now?)
#
# Conditional build:
%bcond_without  dist_kernel	# without kernel from distribution
#
%define		no_install_post_compress_modules	1

%define		_orig_name	eplip
%define		_rel	1

Summary:	EPLIP driver for 2.6.xx kernels
Summary(pl):	Sterownik EPLIP dla kerneli 2.6.xx
Name:		kernel-net-eplip
Version:	0.5.6
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://e-plip.sourceforge.net/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	43019250e7227857ae13bdd39a45494d
Patch0:		eplip-2.6.x.patch
Patch1:		kernel-eplip-WIRING.patch
URL:		http://e-plip.sourceforge.net/
ExclusiveArch:	%{ix86}
PreReq:		modutils
BuildRequires:	rpmbuild(macros) >= 1.118
%{!?_without_dist_kernel:BuildRequires:	kernel-module-build}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
EPLIP (Enhanced Parallel Line IP) module for 2.6.xx kernels.

%description -l pl
Modu³ EPLIP (Enhanced Parallel Line IP) dla j±der 2.6.xx.

%package -n kernel-smp-net-eplip
Summary:	Kernel 2.6.xx SMP module for EPLIP
Summary(pl):	Modu³ SMP j±dra 2.6.xx do obs³ugi EPLIP
Group:		Base/Kernel
Release:	%{_rel}@%{_kernel_ver_str}
PreReq:		modutils >= 2.4.6-4

%description -n kernel-smp-net-eplip
EPLIP (Enhanced Parallel Line IP) SMP module for 2.6.xx kernels.

%description -n kernel-smp-net-eplip -l pl
Modu³ SMP EPLIP (Enhanced Parallel Line IP) dla j±der 2.6.xx.

%prep
%setup	-q -n %{_orig_name}-%{version}
%patch0 -p1
%patch1 -p1
cat <<EOF > Makefile
CONFIG_X86=1
CONFIG_ISA=1
obj-m += eplip.o
eplip-objs := ecp.o eplip-drv.o
EOF

%build
install -d build-done/{UP,SMP}
ln -sf %{_kernelsrcdir}/config-up .config
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules
mv *.ko build-done/UP/

%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 mrproper

ln -sf %{_kernelsrcdir}/config-smp .config
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules

mv *.ko build-done/SMP/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net
cp build-done/UP/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net
cp build-done/SMP/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net

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

%files -n kernel-smp-net-eplip
%defattr(644,root,root,755)
%doc ChangeLog LAME-TESTS README TODO TODO-done WIRING
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/*
