# $Revision: 1.3 $
#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
#
%define		no_install_post_compress_modules	1

%define		_orig_name	eplip
%define		_rel	1

Summary:	EPLIP driver for 2.6.x kernels
Summary(pl):	Sterownik EPLIP dla j±der 2.6.x
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
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_dist_kernel:BuildRequires:	kernel-module-build}
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
%{__make} -C %{_kernelsrcdir} modules \
	SUBDIRS=$PWD \
	O=$PWD \
	V=1
mv *.ko build-done/UP

%{__make} -C %{_kernelsrcdir} mrproper \
	SUBDIRS=$PWD \
	O=$PWD \
	V=1

ln -sf %{_kernelsrcdir}/config-smp .config
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/asm-%{_arch} include/asm
touch include/config/MARKER
%{__make} -C %{_kernelsrcdir} modules \
	SUBDIRS=$PWD \
	O=$PWD \
	V=1

mv *.ko build-done/SMP

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
