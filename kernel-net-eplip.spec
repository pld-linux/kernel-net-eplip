#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution

%define		_orig_name	eplip
%define		pname		kernel-net-eplip
%define		_rel	3

Summary:	EPLIP driver for 2.6.x kernels
Summary(pl.UTF-8):	Sterownik EPLIP dla jąder 2.6.x
Name:		kernel%{_alt_kernel}-net-eplip
Version:	0.5.6
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://e-plip.sourceforge.net/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	43019250e7227857ae13bdd39a45494d
Patch0:		%{pname}-1.patch
Patch1:		kernel-eplip-WIRING.patch
Patch2:		%{pname}-2.patch
Patch3:		%{pname}-module_param_array.patch
Patch4:		%{pname}-2.6.19.patch
Patch5:		%{pname}-2.6.20.patch
Patch6:		%{pname}-2.6.22.patch
Patch7:		%{pname}-2.6.24.patch
Patch8:		%{pname}-autoconf.patch
Patch9:		%{pname}-2.6.32.patch
Patch10:	%{pname}-x64.patch
URL:		http://e-plip.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build}
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
EPLIP (Enhanced Parallel Line IP) driver module for 2.6.x kernels.

%description -l pl.UTF-8
Moduł sterownika EPLIP (Enhanced Parallel Line IP) dla jąder 2.6.x.

%prep
%setup -q -n %{_orig_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

cat <<EOF > Makefile
obj-m += eplip.o
eplip-objs := eplip-drv.o
EOF

%build
%build_kernel_modules -m eplip

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m eplip -d kernel/drivers/net

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc ChangeLog LAME-TESTS README TODO TODO-done WIRING
/lib/modules/%{_kernel_ver}/kernel/drivers/net/*
